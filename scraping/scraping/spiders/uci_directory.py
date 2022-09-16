import datetime
import json
import re
from selenium import webdriver
import requests
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class uci_directory(scrapy.Spider):
    name = 'uci_directory'
    def start_requests(self):

        url = 'https://directory.uci.edu/render-list'

        headers = {
            "authority": "directory.uci.edu",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://directory.uci.edu",
            "referer": "https://directory.uci.edu/query/charl?filter=all",
            "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "Referer": "https://directory.uci.edu/",
            "DNT": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        cookies = {
            "AWSALB": "Z2JPDgulJhUi3hwZ1s+uoa98tqc5jPd/leYoDjsfPzcb0KOIS9OpG//nQQCaQL2bjEMvFAQCkYeXLYvx6fbmzDmTh39E6h2s0yrNJuCDAwe+tl0o9YqDzAzyz2Sr",
            "AWSALBCORS": "Z2JPDgulJhUi3hwZ1s+uoa98tqc5jPd/leYoDjsfPzcb0KOIS9OpG//nQQCaQL2bjEMvFAQCkYeXLYvx6fbmzDmTh39E6h2s0yrNJuCDAwe+tl0o9YqDzAzyz2Sr"
        }

        for name in NamesList:
            body = f'uciKey={name.strip()}&filter=all'

            yield scrapy.Request(
                url=url,
                method='POST',
                dont_filter=True,
                cookies=cookies,
                headers=headers,
                body=body,
                callback=self.parse
            )
    def parse(self, response, **kwargs):
        JData = json.loads(response.text)
        res = scrapy.Selector(text=JData['html'])
        for n in res.css('.collapse.bg-light'):
            detailsUrl = 'https://directory.uci.edu'+n.css('.text-center a::attr(href)').extract_first()
            driver.get(detailsUrl)
            resp = scrapy.Selector(text=driver.page_source)
            item = dict()
            try:
                item['UCInetID'] = [v for v in resp.css('::text').extract() if 'UCInetID' in v][0].split(':')[-1]
            except:
                item['UCInetID'] = ''
            try:
                item['Name'] = [v for v in resp.css('::text').extract() if 'Name' in v][0].split(':')[-1].strip()
            except:
                item['Name'] = ''
            try:
                item['Department']  = [v for v in resp.css('::text').extract() if 'Department' in v][0].split(':')[-1]
            except:
                item['Department'] = ''
            try:
                item['Address'] = [v for v in resp.css('::text').extract() if 'Address' in v][0].split(':')[-1]
            except:
                item['Address'] = ''
            try:
                item['ZOT Code'] = [v for v in resp.css('::text').extract() if 'ZOT Code' in v][0].split(':')[-1]
            except:
                item['ZOT Code'] = ''
            try:
                item['Email'] = [v for v in resp.css('::text').extract() if '@' in v][0]
            except:
                item['Email'] = ''
            try:
                item['Delivery Point'] = [v for v in resp.css('::text').extract() if '@' in v][1]
            except:
                item['Delivery Point'] = ''
            try:
                item['Title'] = [v for v in resp.css('::text').extract() if 'Title' in v][0].split(':')[-1]
            except:
                item['Title'] = ''
            try:
                item['Phone'] = [v for v in resp.css('::text').extract() if 'Phone' in v][0].split(':')[-1]
            except:
                item['Phone'] = ''
            try:
                item['Fax'] = [v for v in resp.css('::text').extract() if 'Fax' in v][0].split(':')[-1]
            except:
                item['Fax'] = ''
            try:
                item['Major'] = [v for v in resp.css('::text').extract() if 'Major' in v][0].split(':')[-1]
            except:
                item['Major'] = ''
            try:
                item["Student's Level"] = [v for v in resp.css('::text').extract() if "Student's Level" in v][0].split(':')[-1]
            except:
                item["Student's Level"] = ''
            csvwriter.writerow(item)
            fileoutput.flush()
    def close(spider, reason):
        driver.quit()
if __name__ == '__main__':
    headers = ['UCInetID', 'Name', 'Department', 'Address', 'ZOT Code', 'Email', 'Delivery Point', 'Title', 'Phone', 'Fax','Major',"Student's Level"]
    fileoutput = open('uci_directory.csv','w', encoding='utf-8', newline='')
    with open('uni_names.txt','r') as fileinput:
        NamesList = fileinput.read().split('\n')
    csvwriter = csv.DictWriter(fileoutput, fieldnames=headers)
    csvwriter.writeheader()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(chrome_options=options)
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(uci_directory)
    process.start()  # the script will block here until the crawling is finished
