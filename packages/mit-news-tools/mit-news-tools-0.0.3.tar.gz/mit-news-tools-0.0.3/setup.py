import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mit-news-tools",
    version="0.0.3",
    author="Emily Fan, Arun Wongprommoon, and Max Tegmark",
    author_email="emilyfan@mit.edu",
    description="tools to help people better understand the news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.mit.edu/Tegmark-Research-Group/mit-news-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        'mitnewstools': ['mitnewstools/*.csv']
    }
)
