from confusables import normalize


def asciify(text: str, return_failed_chars=False):
    """
    Takes a string and returns an ASCII version of it.
    If there is no suitable ASCII version of the string, it will be replaced by a space.

    If return_failed_chars is True, it returns a tuple.
    The first element is the asciified string.
    The second element is a list of characters that failed to be converted into ASCII and instead were converted to spaces.
    example: "asciified string", [":)", ":—)"]

    :param text: A string that you want to make sure is ASCII.
    :param return_failed_chars: If true, will return a list of characters that have failed to convert to ASCII
    :return: an ASCII version of the input string;
            if return_failed_chars is True, it also returns a list of characters that failed to be converted into ASCII
            and instead were converted to spaces
    """
    retstr = ""

    numconvchar = 0
    failedchars = []

    for char in text:
        if not char.isascii():
            newchar = normalize(char, prioritize_alpha=True)[0]

            # attempts to make newchar ascii
            if not newchar.isascii():
                if newchar == '—':
                    newchar = '--'
                    # print("YAY: " + char + " -> "+ newchar)
                else:
                    for posschar in normalize(char):
                        # print(char)
                        if posschar.isascii():
                            newchar = posschar
                            # print("YAY: " + char + " -> "+ newchar)
                            break

            if not newchar.isascii():
                # print("RIP this char cannot be processed: " + char + " -> "+ newchar)

                # print(char.encode('raw_unicode_escape'))
                # print(newchar.encode('raw_unicode_escape'))

                newchar = " "

                failedchars.append(char)

            else:
                numconvchar += 1
            # elif newchar not in ["'", '"', "...", '-']:
            # print("YAY: " + char + " -> "+ newchar)
            retstr += newchar
        else:
            retstr += char

    # print(str(numconvchar) + ' characters conversted to ASCII | ' + str(numfailedchar) + " failed")

    if return_failed_chars:
        return retstr, failedchars
    return retstr


############################### SCRAPING NEWS HOMEPAGE TOOLS #################################################


import requests
from newspaper import Article
import re
from urllib.parse import urlparse
import pandas as pd

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox


def selenium_download(url, driver=None, return_html=True):
    if driver is None:
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='geckodriver', options=options)

    driver.get(url)

    if return_html:
        return driver.page_source

    return driver


def extract_news_urls_selenium(driver, match_file="newsurlpatterns.csv") -> pd.DataFrame:
    all_links = driver.find_elements_by_partial_link_text('')
    url = driver.current_url
    domain = extract_domain(url)

    match_formula = get_match_formula(url, match_file)

    # note that some links will be listed more than once
    news_links = pd.DataFrame(columns=["url", "x", "y", 'width', 'height', 'area'])

    for link in all_links:
        base_url = extract_base_url(link.get_property('href'))
        if is_news_article(base_url, domain, match_formula):
            news_links.append(
                {'url': base_url, 'x': link.location['x'], 'y': link.location['y'],
                 'width': link.size['width'], 'height': link.size['height'],
                 'area': link.size['width'] * link.size['height']}, ignore_index=True)

    return news_links


def extract_base_url(url: str, endswithslash=True) -> str:
    """
    Return a url that cuts off the item after the ?
    If endswithslash is True, returns a url that ends with a slash
    """
    # NOT FOR ARTICLES
    parsed_url = urlparse(url)
    base_url = 'https://' + parsed_url.netloc + parsed_url.path
    if endswithslash and not base_url.endswith('/'):
        base_url = base_url + '/'

    return base_url


def extract_domain(url: str) -> str:
    """
    Extracts the domain of a site.
    For instance, "https://www.economist.com/news/2020/06/19/frequently-asked-questions"
    becomes "economist.com"
    """
    if not (url.startswith('http://') or url.startswith('https://')):
        url = '//' + url

    domain = urlparse(url).netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    return domain


def extract_urls(html: str, base_url: str) -> list:
    """
    Given the html and the url of a news homepage,
    return a list of urls that the homepage links to.
    """
    # format domain like this: https://www.economist.com/
    base_url = extract_base_url(base_url)

    # search for urls
    common_search = [r"href=\\?\"[^\" ]*\\?\"", r"href=\\?\'[^\' ]*\\?\'", r"\"uri\":\"[^\" ]*\"",
                     r"\"url\":\"[^\" ]*\""]
    search = '|'.join(common_search)
    matches = re.findall(search, html)

    hrefs = []

    # process urls to make i
    for match in matches:
        # print("match:" + match)
        match = match.replace('\\\"', '\"')  # print('\\\"') leads to this: \"
        match = match.replace('\\/', '/')
        # print(match)
        match = re.split(r'\"|\'', match)[-2]
        # print(match)
        if (match is not None):

            if (match[:7] == 'http://'):
                to_append = match

            elif (match[:8] == 'https://'):
                to_append = match
            elif (match[:2] == '//'):
                to_append = match[2:]
            elif (match[:1] == '/'):
                to_append = base_url + match[1:]
            else:
                to_append = base_url + match

            if to_append not in hrefs:
                hrefs.append(to_append)

    return hrefs


# TODO to test this method
def get_match_formula(domain, file='newsurlpatterns.csv'):
    domain = extract_domain(domain)

    newsurlpatterns = pd.read_csv(file)
    match_formula = newsurlpatterns[newsurlpatterns['url'].str.contains(domain)]['pattern']

    if len(match_formula) == 0 or match_formula.isna().any():
        match_formula = set(newsurlpatterns['pattern'])
        match_formula = {f for f in match_formula if pd.notna(f)}

    return match_formula


def is_news_article(url: str, domain: str, match_formula='newsurlpatterns.csv', blacklist=None) -> bool:
    """
    :param url: url of what is possibly an article.
    :param domain: the domain name of the newssite that the url should belong to
    :param match_formula: (optional) a list of regular expressions such that the url matches at least one of them
    :param blacklist: (optional) A list of regular expressions that the url should not follow
    :return: True if the url is a news article from the same domain on the website
    """
    # format domain like this washingtonpost.com
    domain = extract_domain(domain)

    if blacklist is None:  # TODO make blacklist a csv file or something
        blacklist = [
            r"^.*.png.*$",  # thecanary, motherjones
            r"^.*.jpg.*$",  # infowars
            r"^.*privacy-policy.*$",  # spectator, cbsnews
            r"^.*commons-community-guidelines$",  # commondreams
            r"^.*contact-us.*$",  # consortiumnews
            r"^https?://theconversation.com/institutions/.*$",  # theconversation
            r"^https?://theconversation.com/us/partners/.*$",  # theconversation
            r"^https?://theconversation.com/profiles/.*$",  # theconversation
            r"^(podcasts|itunes).apple.com/.*$",  # dailycaller
            # r"^.*facebook.com/.*$", #aljazeera, americanthinker, ap
            # r"^.*twitter.com/.*$", #aljazeera, ap
            # r"^.*snapchat.com/.*$", #nbcnews
            # r"^.*plus.google.com/.*$", #breitbart
            r"^mailto:.*$",  # ap
            r"^.*/aboutus/.*$",  # aljazeera
            r"^.*/terms-of-service/.*$",  # spectator
            r"^spectator.org/category/.*$",  # spectator
            r"^.*/about-breitbart-news.pdf$",  # breitbart
            # r"^coverageContainer/.*$", #cnn
            r"^.*/comment-policy/$",  # consortiumnews
            r"^.*/frequently-asked-questions$",  # economist
            r"^.*brand-use-policy$",  # eff
            r"^.*rss-feed.*$",  # fivethirtyeight
            r"^.*cookies-policy.*$",  # fivethirtyeight
            r"^.*career-opportunities.*$",  # foreignaffairs
            r"^.*my.*account.*$",  # foreignaffairs
            r"^.*foxnews.com/category/.*$",  # foxnews
            r"^.*mobile-and-tablet$",  # theguardian
            r"www.lewrockwell.com/books-resources/murray-n-rothbard-library-and-resources/",  # lewrockwell
            # r"^.*podcast.*$",  # too restrictive, if the news is about a podcast, it registers as not news
            # nationalreview  # https://www.usatoday.com/story/entertainment/celebrities/2020/08/18/michelle-obama-brother-reveals-first-thoughts-barack-podcast/5584158002/
            r"^.*disable.*ad.*blocker.*$",  # slate
            r"^./category/.*$",
        ]

    if type(match_formula) is str:
        match_formula = get_match_formula(domain, match_formula)

    if domain not in url:
        return False

    for formula in blacklist:
        if re.match(formula, url) is not None:
            return False

    for formula in match_formula:
        formula = formula[2:-1]  # to get rid of the r^"" and only get the stuff in the middle
        if re.match(formula, url) is not None:
            return True

    return False


def filter_article_urls(urls: list, domain: str, match_file='newsurlpatterns.csv') -> list:
    """
    :param urls: list of urls
    :param domain: domain the url should be in
    :param match_file: (optional) file that contains a list of regular expressions for news articles
    :return: a list of urls that are news articles and come from the specified domain
    """
    # add the global file system later it's so we don't have to load it everytime

    domain = extract_domain(domain)

    # newsurlpatterns = pd.read_csv(match_file)

    # common blacklist now in is_news_url, so commented out here
    # common_blacklist = [
    #     r"^.*.png.*$",  # thecanary, motherjones
    #     r"^.*.jpg.*$",  # infowars
    #     r"^.*privacy-policy.*$",  # spectator, cbsnews
    #     r"^.*commons-community-guidelines$",  # commondreams
    #     r"^.*contact-us.*$",  # consortiumnews
    #     r"^https?://theconversation.com/institutions/.*$",  # theconversation
    #     r"^https?://theconversation.com/us/partners/.*$",  # theconversation
    #     r"^https?://theconversation.com/profiles/.*$",  # theconversation
    #     r"^(podcasts|itunes).apple.com/.*$",  # dailycaller
    #     # r"^.*facebook.com/.*$", #aljazeera, americanthinker, ap
    #     # r"^.*twitter.com/.*$", #aljazeera, ap
    #     # r"^.*snapchat.com/.*$", #nbcnews
    #     # r"^.*plus.google.com/.*$", #breitbart
    #     r"^mailto:.*$",  # ap
    #     r"^.*/aboutus/.*$",  # aljazeera
    #     r"^.*/terms-of-service/.*$",  # spectator
    #     r"^spectator.org/category/.*$",  # spectator
    #     r"^.*/about-breitbart-news.pdf$",  # breitbart
    #     # r"^coverageContainer/.*$", #cnn
    #     r"^.*/comment-policy/$",  # consortiumnews
    #     r"^.*/frequently-asked-questions$",  # economist
    #     r"^.*brand-use-policy$",  # eff
    #     r"^.*rss-feed.*$",  # fivethirtyeight
    #     r"^.*cookies-policy.*$",  # fivethirtyeight
    #     r"^.*career-opportunities.*$",  # foreignaffairs
    #     r"^.*my.*account.*$",  # foreignaffairs
    #     r"^.*foxnews.com/category/.*$",  # foxnews
    #     r"^.*mobile-and-tablet$",  # theguardian
    #     r"www.lewrockwell.com/books-resources/murray-n-rothbard-library-and-resources/",  # lewrockwell
    #     # r"^.*podcast.*$",  # too restrictive, if the news is about a podcast, it registers as not news
    #     # nationalreview  # https://www.usatoday.com/story/entertainment/celebrities/2020/08/18/michelle-obama-brother-reveals-first-thoughts-barack-podcast/5584158002/
    #     r"^.*disable.*ad.*blocker.*$",  # slate
    #     r"^./category/.*$",
    # ]

    common_formula = get_match_formula(domain, match_file)

    filtered_urls = []
    for url in urls:
        # TODO perhaps change the url so that the ?# parts get left out
        if is_news_article(url, domain, common_formula):
            filtered_urls.append(url)

    return filtered_urls








############################### SCRAPE DATE INFO #############################################
import pandas as pd
import re

import datetime
import datefinder
from date_guesser import guess_date, Accuracy

# uncommented this because some newspapers like psychology today
# don't have the json format
def datefind_html(article_html: str, url: str, map_file="datemap.csv") -> str:  # rename to _html
    """
    Given the html and url of a news article,
    return the date published in isoformat or an empty string if date cannot be found
    """
    def find_html_in_between(articlehtml: str, keyhtml: str):
        if keyhtml not in articlehtml:
            return None

        startindex = articlehtml.index(keyhtml)
        dateindex = 0

        numopen = 1
        endindex = -1

        for i in range(startindex + len(keyhtml) - 1, min(startindex + 1000, len(articlehtml))):
            if dateindex == 0 and articlehtml[i] == '>':
                dateindex = i + 1

            if articlehtml[i] == '<' and i + 1 < len(articlehtml):
                # print('numopen ' + str(numopen))
                # print('art i+1: ' + articlehtml[i + 1])
                if articlehtml[i + 1] == '/':
                    numopen -= 1
                else:
                    numopen += 1

            if numopen == 0:
                endindex = i
                break

        return articlehtml[dateindex: endindex]

    datemap = pd.read_csv(map_file, index_col=0)

    html_pattern = datemap['htmlparent'][datemap['domain'].apply(lambda domain: domain in url)]

    if html_pattern.size == 1:
        html_pattern = html_pattern.iloc[0]
        dateraw = find_html_in_between(article_html, html_pattern)
        # print(dateraw, newscuesdf[newssource][0])  for debugging purposes
        try:
            dateparsed = next(datefinder.find_dates(dateraw))
            return dateparsed.isoformat()
        except:
            return ""

    return ""  # add this so that it is guaranteed to return something


# Returns a dictionary in the form
# {'datePublished': '2020-06-29T18:51:27-04:00', 'dateModified': '2020-06-29T19:52:56-04:00'}
def datefind_json(article_html: str) -> dict:  # rename to _json
    """
    Given the html of a news article,
    return a dictionary with keys that starts with date, if found, such as datePublished, dateModified, or dateCreated.
    The values of the dictionary should be in isoformat. If such keys are not found, it returns an empty dictionary.
    """
    retval = re.findall(r"[\"\']date\w+[\"\']:\s*[\"\'][\w\-:\.\+]+[\"\']", article_html)
    if len(retval) == 0:
        return {}
    # format so items compatible with pandas DataFrame:
    retval = list(map(lambda s: re.split(r'[\"\'\s]+', s)[1::2], retval))
    retval = pd.DataFrame(retval)
    retval = retval.sort_values(1).drop_duplicates(0).set_index(
        0)  # sort by dates in old-new order and keep oldest dates
    retval = retval.to_dict()[1]
    return retval


def get_dates(article_html: str, url: str) -> tuple:
    """
    Given the html and the url of the url,
    return the publication date and the modification date in isoformat as a tuple.

    # format is (date_published_iso, date_modified_iso)

    ("2020-05-27T21:59:25+01:00", "2020-05-28T18:34:13+01:00")

    If either of the publication date or the modification date cannot be found, they will be a
    empty string in the tuple.

    For instance, here is the example if the modification date was not found

    ("2020-05-27T21:59:25+01:00", "")

    How it works:

    1) Looks for date in a website's json.

    2) If date not found, look for date in url.

    3) If date still not found, look for date in html.

    4) Use media cloud's dateguesser.
    """
    # first try the json method
    datedict = datefind_json(article_html)  # method name changed
    pubtime = datedict.get("datePublished", '')
    modtime = datedict.get("dateModified", "")

    # print("Go JSON", datedict)  # add print statement

    # add html to try because some news sources like psychology today only has html way of scraping
    if pubtime == "":
        pubtime = datefind_html(article_html, url)

        # print("Go HTML", pubtime)  # add print statement

    # now, try to look at the url
    url_date = re.search(
        r"(19|20)\d{2}[/\-_]"  # year
        r"[0-1]?\d[/\-_]"  # month
        r"[0-3]?\d",  # day
        url)

    if url_date is not None:
        date_found = re.split(r"[/\-_]", url_date.group())
        year = int(date_found[0])
        month = int(date_found[1])
        day = int(date_found[2])
        pubtime = datetime.date(year, month, day).isoformat()

        # print('Go url!', pubtime)

    # add date-guesser
    if pubtime == "":
        guess = guess_date(url, article_html)
        if guess.accuracy == Accuracy.DATE or guess.accuracy == Accuracy.DATETIME:
            pubtime = guess.date.isoformat()
            # print(guess.date.isoformat()[:19], guess.method)
            # print("Go dateguesser", pubtime, guess.method)
        elif guess.accuracy == Accuracy.PARTIAL:
            pubtime = guess.date.isoformat()[:7]
            # print("Go dateguesser", pubtime, guess.method)
            # print(guess.accuracy, guess.method, guess.date.isoformat()[:7])
        # else:
        # print(guess.accuracy, guess.method, guess.date)

    return pubtime, modtime


if __name__ == "__main__":
    url = "https://www.cnn.com/2020/06/16/politics/cia-wikileaks-vault-7-leak-report/index.html"
    # import requests
    # page = requests.get(url)
    # emily_datefind_html(page.text, url)

    from newspaper import Article
    art = Article(url)
    art.download()
    print(get_dates(art.html, url))