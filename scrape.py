# -*- coding: utf-8 -*-

import os
import sys
import threading
import urllib
import urllib2
import cookielib
import smtplib
import ftplib
import datetime
import time
import bs4
import re
import csv
import numpy
from PIL import Image
import random
from bs4 import BeautifulSoup as soup
import pandas as pd

def request_and_parse():
    hdr = random.choice([hdr1, hdr2, hdr3, hdr4, hdr5])
    req = urllib2.Request(site, headers=hdr)

    # Added cookie handling function while url opening due to new myntra weird redirect behaviour
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    response = opener.open(req)
    content = response.read()
    response.close()

    return content


# make sure rows = 500 and p = 1 ex - https://www.myntra.com/amp/men-tshirts?rows=500&p=1
# https://www.myntra.com/amp/nehru-jackets?rows=500&p=1,https://www.myntra.com/amp/helmet?rows=500&p=1
site = "https://www.myntra.com/amp/men-shirts?rows=500&p=1"

hdr1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
hdr2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
hdr3 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
hdr4 = {'User-Agent': 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
hdr5 = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

content = request_and_parse()

page_soup = soup(content, "html.parser")
contains_info = page_soup.findAll("div", {"class": "productInfo"})
contains_url = page_soup.findAll("div", {"class": "product"})

y = len(contains_info)

a = 0

filename = "product_info.csv"
f = open(filename, "w")
headers = "Product_name,Brand,Image_url\n"
f.write(headers)

filename2 = "image_urls.csv"
opening = open(filename2, "w")

while y != 0:
    for each_product in contains_info:

        product_name = each_product.findAll("h4", {"class": "name-product"})
        product_name = product_name[0].text.strip()
        product_name = str(product_name.encode('utf-8', 'replace'))

        brand = each_product.findAll("div", {"class": "name"})
        brand = brand[0].text
        brand = str(brand.encode('utf-8', 'replace'))

        data1 = product_name + "," + brand + "\n"
        f.write(data1)
    
    print("Populated product_info.csv")

    myntra_homepage = "https://www.myntra.com"

    for each_product in contains_url:
    
        product_link = str(each_product.a["href"])
        product_link = myntra_homepage + product_link
        each_image_url = each_product.findAll("amp-img")[0].get('src')
        data2 = each_image_url + ";"
        opening.write(data2)

    print("Populated image_urls.csv")

    if a == 100:
            site = str(site[0:-2]) + str(a)
    elif a > 100:
            site = str(site[0:-3]) + str(a)
    elif a <= 10:
        #     code will crash if the no of product listed at myntra in a specific category exceeds500000
            site = str(site[0:-1]) + str(a)
    elif 10 < a <= 99:
            site = str(site[0:-2]) + str(a)

    a = int(a)
    a = a + 1
    print("At Page" + str(a))

    if a > 20:
            break

    # hdr = random.choice([hdr1, hdr2, hdr3, hdr4, hdr5])
    # req = urllib2.Request(site, headers=hdr)
    # cj = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # response = opener.open(req)
    # content = response.read()
    # response.close()
    content = request_and_parse()

    page_soup = soup(content, "html.parser")
    contains_info = page_soup.findAll("div", {"class": "productInfo"})
    contains_url = page_soup.findAll("div", {"class": "product"})
    y = len(contains_info)
