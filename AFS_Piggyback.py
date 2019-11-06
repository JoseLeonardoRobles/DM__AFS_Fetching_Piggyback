#!/usr/bin/env python
'''
====================================================================================================================
Complutense University Of Madrid
Astrophysics Department
PhD's Project: To Statistically Study the Seasonal Night Sky Brightness and Color Evolution in Madrid.
Directors: - Ph.D. Jaime Zamorano
           - Ph.D. Sergio Pascual
Script Developed By: Jose Robles, Ph.D. student  email: josrob01@ucm.es

ASTMON Script tasks: 1_Connect to URL 
                     2_Piggyback: download all files with dot extention (e.p: .fit, .dat,.html, .png, and .fit)
                     3_Acces URL's directories recursively
                     4_Apply Piggyback
                     5_Re-Construct Trees Full Hierarchy
                     6_Upload info to Google Drive via R-Clone


====================================================================================================================
'''
import urllib
import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import shutil
import requests
import json
import os



URL ='http://147.96.21.177/20190912/'

#1] Check Url Connectivity-Status, And Parsing URL html Data
start_url = URL
r = requests.get(start_url)
soup = BeautifulSoup(r.text,'html.parser')
print('---BEAUTIFULSOUP CONTENT---\n',soup)

#2] Get url Tags and Useful Information
pre = soup.find('pre')
print('---Pre---\n',pre) 

#3] Picking Out a[href]
file_urls_select = pre.select('a[href*="."]') 
full_urls = [urljoin(start_url, url['href'])for url in file_urls_select]
print(full_urls,type(full_urls))


#4] Downloading files (Piggyback).
def Piggyback(URL,full_urls):
    """ Piggyback: Download Files With Any Dot Extention (e.p: .fit, .dat,.html, .png, and .fit)
    Parameters
    ----------
    URL : Parent URL
        E.p: http://147.96.21.177/
    full_urls : Comprehensive List Containing Urls From Parent URL 

    Returns
    -------
    Callable Function : Piggyback
        Download All The Files on URL (e.p: .fit, .dat,.html, .png, and .fit)
    """
    for full_url in full_urls:
        file_name = full_url.split('/')[-1]
        print(full_url)
        print("Downloading {} To {}...".format(full_url, 'Working Directory'))
        with urllib.request.urlopen(full_url) as response, open(file_name, 'wb') as out_file: 
            shutil.copyfileobj(response, out_file)
        print('Done')

Piggyback(URL,full_urls)
 
#5] Access Urls Recursively (wag_and_follow).
file_urls_select_Folders = pre.select('a[href]') 
full_urls = [urljoin(start_url, url['href'])for url in file_urls_select_Folders]
for x in full_urls:
    file_name = x.split('/')[-1]
    print("Selecting {} {}...".format(x, 'From Parent URL'))

def wag_and_follow(url_list, crawled_urls, driver, URL):
    """ Get webside urls and crawl each url recursively"""

'''
**Spiders**

Spiders are classes which define how a certain site (or a group of sites) will be scraped 
(extracting data from websites), including how to perform the crawl (i.e. follow links)
and how to extract structured data from their pages (i.e. scraping items).

**Feed exports**
New in version 0.10.

One of the most frequently required features when implementing scrapers is being able 
store the scraped data properly and, quite often, that means generating an “export file” 
with the scraped data (commonly called “export feed”) to be consumed by other systems.

Scrapy provides this functionality out of the box with the Feed Exports, which allows you
to generate a feed with the scraped items, using multiple serialization formats and storage
backends.

Serialization formats
For serializing the scraped data, the feed exports use the Item exporters. 
These formats are supported out of the box:

- JSON
- JSON lines
- CSV
- XML

**Pipeline**

Pipeline is just an abstract notion, it's not some existing ml algorithm. Often in ML tasks 
you need to perform sequence of different transformations (find set of features, generate new features, 
select only some good features) of raw dataset before applying final estimator.

**Item Pipeline**
After an item has been scraped by a spider, it is sent to the Item Pipeline which
processes it through several components that are executed sequentially.

Typical uses of item pipelines are:

- cleansing HTML data
- validating scraped data (checking that the items contain certain fields)
- checking for duplicates (and dropping them)
- storing the scraped item in a database

'''
