import csv
import datetime
import re
import csvdiff
import requests as requests
import scrapy
import random
from colour import Color
from scrapy.crawler import CrawlerProcess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

cwd = os.getcwd()
proxy_file = open('proxy.txt', 'r')
proxies = proxy_file.read().split('\n')
proxies = [p for p in proxies if p]

def get_proxies():
    proxy = random.choice(proxies)
    return proxy
def get_driver():
    random_proxy = get_proxies()
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-javascript')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--width=1024')
    # options.add_argument('--height=768')
    chrome_capabilities = webdriver.DesiredCapabilities.CHROME
    # chrome_capabilities['marionette'] = True
    chrome_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": random_proxy,
        # "ftpProxy": random_proxy,
        # "sslProxy": random_proxy
    }
    driver = webdriver.Chrome(desired_capabilities=chrome_capabilities, chrome_options=options)
    return driver


if __name__ == '__main__':
    fileread = open('profiles.csv', 'r', encoding='utf-8')
    csvreader = csv.reader(fileread, delimiter=',')
    urllist = []
    header = ['url', 'name','posts','followers']
    filewrite = open('insta_profile_output.csv', 'w', newline='', encoding='utf-8')
    filewriter = csv.DictWriter(filewrite, fieldnames=header)
    filewriter.writeheader()
    driver = get_driver()
    for row in csvreader:
        # name_.append(row[0]+'*'+row[1])
        urllist.append(row[0] + '*' + row[1])
    for url in urllist[1:]:
        start = time.time()
        driver.get(url.split('*')[0])
        resp = scrapy.Selector(text=driver.page_source)
        item = dict()
        item['url'] = url.split('*')[0]
        item['name'] = url.split('*')[1]
        item['posts'] = resp.css('#react-root > section > main > div > header > section > ul > li:nth-child(1) > a > div > span::text').extract_first()
        item['followers'] = resp.css('#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > div > span::text').extract_first()
        end = time.time()
        print(end - start)
        filewriter.writerow(item)
        filewrite.flush()