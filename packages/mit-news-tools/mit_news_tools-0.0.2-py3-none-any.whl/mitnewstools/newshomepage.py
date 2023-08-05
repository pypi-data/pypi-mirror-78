"""
On second thought, I suggest that you simply make a single package installable with
   pip install mit-news-tools
that includes all the functions we discussed as well as dateguesser:

def download(url): #  returns html

def dateguesser(html): # returns [publication date, ...]

def extract_html(html): # Return lists of URLs found in the html

def classify_url(parent_url,url): # Returns [True/False,... perhaps additional info]

Does that sound good?
:-)

ASCIIFY method can be added here as well
"""
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


def requests_download(url, return_html=True):
    """
    Use the requests package to download the html version of the

    :param url:
    :param return_html:
    :return:
    """
    page = requests.get(url)  # TODO do something about error responses
    if return_html:
        return page.text
    return page


def news3k_download(url, return_html=True):
    art = Article(url)
    art.download()
    if return_html:
        return art.html
    return art


def selenium_download(url, driver=None, return_html=True):
    if driver is None:
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='geckodriver', options=options)

    driver.get(url)

    if return_html:
        return driver.page_source

    return driver


def extract_news_urls_selenium(driver, match_file="newsurlpatterns.csv"):
    all_links = driver.find_elements_by_partial_link_text('')
    url = driver.current_url
    domain = extract_domain(url)

    match_formula = get_match_formula(url, match_file)

    # note that some links will be listed more than once
    news_links = pd.DataFrame(columns=["url", "x", "y", 'width', 'height', 'area'])

    for link in all_links:
        base_url = extract_base_url(link.get_property('href'))
        if is_news_url(base_url, domain, match_formula):
            news_links.append(
                {'url': base_url, 'x': link.location['x'], 'y': link.location['y'],
                 'width': link.size['width'], 'height': link.size['height'],
                 'area': link.size['width'] * link.size['height']}, ignore_index=True)

    return news_links


def extract_base_url(url: str, endswithslash=True):
    # NOT FOR ARTICLES
    parsed_url = urlparse(url)
    base_url = 'https://' + parsed_url.netloc + parsed_url.path
    if endswithslash and not base_url.endswith('/'):
        base_url = base_url + '/'

    return base_url


def extract_domain(url: str):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = '//' + url

    domain = urlparse(url).netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    return domain


def extract_urls(html: str, base_url: str):  # todo rename domain to baseurl
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


def is_news_url(url: str, domain: str, match_formula='newsurlpatterns.csv', blacklist=None):
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


def filter_article_urls(urls: list, domain: str, match_file='newsurlpatterns.csv'):
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
        if is_news_url(url, domain, common_formula):
            filtered_urls.append(url)

    return filtered_urls


# requests, news3k, selenium
if __name__ == "__main__":
    medialist = pd.read_csv('../Project-C/Arun/GNewsCorpus/medialist1.csv', header=None)
