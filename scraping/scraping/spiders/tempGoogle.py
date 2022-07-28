import re
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from urllib.parse import urlparse
import mysql.connector
import json
from copy import deepcopy
import datetime,time
import csv
# from googlesearch import search
import pyautogui as pt
from selenium import webdriver
driver =webdriver.Firefox()

API_KEY = 'd0684417c4d70f3b14308e6833732a4d'  ## Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup

csv_columns = ['name', 'email', 'phone', 'phone2', 'company', 'city', 'country', 'link', 'designation',
               'industry']
csvfile = open('csv_files.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def create_google_url(query, site=''):
    google_dict = {'q': query}
    # google_dict = {'q': query, 'num': 100, }
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
        return 'https://www.google.com/search?' + urlencode(google_dict)
    return 'https://www.google.com/search?' + urlencode(google_dict)


# class CustomProxyMiddleware(object):
#     def process_request(self, request, spider):
#         request.meta["proxy"] = "5.79.66.2:13010"
#
# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "en-US",
#     "cache-control": "max-age=0",
#     "cookie": "CGIC=EhQxQzFDSEJGX2VuUEs5MTFQSzkxMyKHAXRleHQvaHRtbCxhcHBsaWNhdGlvbi94aHRtbCt4bWwsYXBwbGljYXRpb24veG1sO3E9MC45LGltYWdlL2F2aWYsaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOQ; ANID=AHWqTUm3o5sHnpm1d7ETNl4XyNKzT5E7NzPtN5jxx1OkTLysUYSACPsHVNqUbHiL; SEARCH_SAMESITE=CgQI9JAB; CONSENT=YES+PK.en-GB+20161218-19-0; OTZ=5764884_36_36__36_; OGP=-4061129:; HSID=ALQCkGsssmUZfSZMm; SSID=AStVNnKvEs77Vi2iX; APISID=l7joSl2EffhVqC6c/Ao7XrYqOwE-sTkAOi; SAPISID=nUx1lRE1tFFnibr8/AO8D7-VlZuKN34oY6; __Secure-3PAPISID=nUx1lRE1tFFnibr8/AO8D7-VlZuKN34oY6; SID=5ge-ndyVPDG_xCzFZZNUzF3ODU9UlDSfkYKzwbJB_QN9gS1w5sKE-Q0WelEsP_keHXIp2Q.; __Secure-3PSID=5ge-ndyVPDG_xCzFZZNUzF3ODU9UlDSfkYKzwbJB_QN9gS1wsxQbM9aWUT-4yOIV83iX_Q.; SIDCC=AJi4QfH86ZviiP1PG6tAhW__FgPTXWXjFjzGf4k-lwyjxIC8qNZfu-PeyBhOLkVixsvmTX38hdM; __Secure-3PSIDCC=AJi4QfFPb5xR6Kts_NOP_wSr1O8Q9ZoMVmHVyDqlZc_y-C_XhLdAyKlbNtLpwDClUjCRSDymWQ; NID=207=Dq-4x93gPoh-ZuJAvNu7UMANlqzK9w9rIL6u-bx_bSpWwIJyfqmAb6LqJ0TGjVVE3BY-PuYzxB4OsbDSf0QWQoj0U5j3QOaBAhvNiAQPQEuPkGZ3CQQn09StOXEXuOCIfBbEM3_l4hYX0YDrDeJ08Gg1qhI31qlgCPYiczZAY1ecKeGxjlNzqJNykYLnOf4CGWLoktBEoUuZ4w07Xn74cHr9MYzCdlC6oszvRRxrBNQHcw; 1P_JAR=2021-01-14-12; DV=88AxTg5YL5Us4I4-5ZYxV2qQ5U0NcFc8_s6VasskMwAAAAA",
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-user": "?1",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
#     "x-client-data": "CJC2yQEIo7bJAQjBtskBCKmdygEIxsLKAQisx8oBCLTLygEIpM3KAQjc1coBCJSaywEI1ZzLAQioncsBCKqdywEY+rjKAQ==",
#     'Decoded': "message ClientVariations {// Active client experiment variation IDs.repeated int32 variation_id = [3300112, 3300131, 3300161, 3313321, 3318086, 3318700, 3319220, 3319460, 3320540, 3329300, 3329621, 3329704, 3329706]; // Active client experiment variation IDs that trigger server-side behavior.repeated int32 trigger_variation_id = [3316858];}"
#
#     }


class GoogleSpider(scrapy.Spider):
    name = 'google'

    allowed_domains = ['api.scraperapi.com']
    # headers={ "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    # "Dnt": "1",
    # "Host": "httpbin.org",
    # "Upgrade-Insecure-Requests": "1",
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    # "X-Amzn-Trace-Id": "Root=1-5ee7bae0-82260c065baf5ad7f0b3a3e3"}
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': ['429']
    }
    proxy = 'http://d0684417c4d70f3b14308e6833732a4d@proxy-server.scraperapi.com:8001/'
    # proxy = 'http://5.79.66.2:13010'
    # proxy1 = 'https://5.79.66.2:13010'
    cities = []
    designations = []
    industries = []
    current_index = 0
    url_template = 'http://api.scraperapi.com?api_key=d0684417c4d70f3b14308e6833732a4d&url={}'
    connection = None
    cursor = None
    count = 0
    csv_count = 0

    def get_connection(self):
        self.connection = mysql.connector.connect(host='104.155.184.16',
                                                  database='scraping',
                                                  user='root',
                                                  password='Password123$')
        self.cursor = self.connection.cursor()

    def get_cities(self):
        file_ = open('cities_orig.csv', 'r', encoding='ISO-8859-1')
        city_rows = file_.read()
        city_rows = city_rows.split('\n')
        cities = []
        for city_row in city_rows:
            city_row = city_row.split(',')
            cities.append(city_row)
        return cities

    def get_designations(self):
        file_ = open('designations.csv', 'r', encoding='ISO-8859-1')
        designation_rows = file_.read()
        designation_rows = designation_rows.split('\n')
        designations = []
        for designation_row in designation_rows:
            designation_row = designation_row.split(',')
            if len(designation_row) > 1:
                designations.append(designation_row[1])
        return designations

    def get_industries(self):
        file_ = open('designations.csv', 'r', encoding='ISO-8859-1')
        designation_rows = file_.read()
        designation_rows = designation_rows.split('\n')
        designations = []
        for designation_row in designation_rows:
            designation_row = designation_row.split(',')
            designations.append(designation_row[0])
        return designations

    def start_requests(self):

        self.get_connection()
        self.cities = self.get_cities()
        self.designations = self.get_designations()
        self.industries = self.get_industries()
        for city in self.cities:
            if len(city) > 1:
                for designation in self.designations:
                    for industry in self.industries:
                        designation = designation.split('and')[0]
                        designation = designation.split('And')[0]
                        # query = 'site:http://linkedin.com/in/ intitle:"{designation}" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "{city}" AND "{industry}"'.format('ceo', '{}, {}'.format('london', 'united kingdom'))
                        # query = 'site:http://linkedin.com/in/ intitle:"ceo" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "london" AND ("information technology" OR "software")'
                        query = 'site:http://linkedin.com/ intitle:"{}" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "{}" AND "{}"'.format(
                            designation, city[0].replace('"', ''), industry)
                        driver.get('https://www.google.com/')
                        time.sleep(2)
                        pt.typewrite(query)
                        time.sleep(1)
                        pt.press('enter')
                        time.sleep(3)

                        # url = create_google_url(query)
                        yield scrapy.Request(url =driver.current_url, callback=self.parse, meta={'pos': 0, 'city': city,
                                                                                              'query': query, 'start': 100,
                                                                                              'industry': industry,
                                                                                              'designation': designation})

    def parse(self, response):

        items = []
        industry = response.meta['industry']
        designation = response.meta['designation']
        start = deepcopy(response.meta['start'])
        city = response.meta['city']
        print(response.status)
        print(response.meta['url'])
        if response.status != 200:
            time.sleep(3)
            yield scrapy.Request(response.url, callback=self.parse, meta={'pos': 0, 'city': city,
                                                                          'url': response.meta['url'], 'start': start,
                                                                          'industry': industry,
                                                                          'designation': designation,
                                                                          'proxy': self.proxy},
                                 dont_filter=True)
            return
        values_str = ''
        if len(response.css('.tF2Cxc')) > 99:
            url = '{}&start={}'.format(response.meta['url'], response.meta['start'])
            yield scrapy.Request(url, callback=self.parse,
                                 meta={'pos': 0, 'city': city, 'url': response.meta['url'], 'start': start + 100,
                                       'industry': industry, 'designation': designation, 'proxy': self.proxy},
                                 dont_filter=True)
        for result in response.css('.tF2Cxc'):
            item = dict()
            item['city'] = city[0].replace('"', '')
            item['country'] = city[1].replace('"', '')
            item['link'] = result.css('a ::attr(href)').extract_first('').replace('"', '')
            heading = result.css('a ::text').extract_first('')
            item['company'] = heading.split('-')[-1].split('|')[0].replace('"', '')
            item['name'] = heading.split('-')[0].replace('"', '') if heading.split('-') else ''

            text = ' '.join(result.css('::text').extract())
            emails = [v for v in text.replace('@ ', '@').split(' ') if '@' in v and '.' in v]
            emails = list(set(emails))
            item['email'] = emails[0] if emails else ''
            item['email'] = item['email'].split(':')[1] if ':' in item['email'] else item['email']
            item['email'] = item['email'].split('|')[1] if '|' in item['email'] else item['email']
            item['email'] = item['email'][:item['email'].find('.com') + 4] if '.com' in item['email'] else ''
            item['email'] = item['email'].replace('"', '')
            try:
                if (item['email'][0].isnumeric()) or (item['email'][0].isalpha()):

                    item['email'] = item['email']
                else:
                    item['email'] = ''
            except:
                pass
            phones = ', '.join(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)).split(',')

            item['phone'] = phones[0].replace('"', '') if phones else ''
            try:
                if len(item['phone']) > 8:
                    item['phone'] = item['phone'].replace(" ", '')
                else:
                    item['phone'] = ''
            except:
                pass
            item['phone2'] = phones[1].replace('"', '') if len(phones) > 1 else ''
            try:
                if len(item['phone2']) > 8:
                    item['phone2'] = item['phone2'].replace(" ", '')
                else:
                    item['phone2'] = ''
            except:
                pass
            item['industry'] = industry.replace('"', '')
            item['designation'] = designation.replace('"', '')
            items.append(item)

            values_str = '{}("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"),'.format(values_str, item['name'],
                                                                                         item['email'],
                                                                                         item['phone'], item['phone2'],
                                                                                         item['company'], item['city'],
                                                                                         item['country'], item['link'],
                                                                                         industry, designation)
            for item in items:
                writer.writerow(item)
                csvfile.flush()
        # if response.css('.tF2Cxc'):
        #     self.count += len(response.css('.tF2Cxc'))
        #     print('got data: {} total: {}'.format(len(response.css('.tF2Cxc')), self.count))
        #     mySql_insert_query = "INSERT IGNORE INTO data (name, email, phone, phone2, company, city, country, link, industry, designation) VALUES {}".format(
        #         values_str[:-1])
        #     try:
        #         self.cursor.execute(mySql_insert_query)
        #
        #         print('insert')
        #         for item in items:
        #             writer.writerow(item)
        #             csvfile.flush()
        #     except Exception as e:
        #         self.csv_count += len(items)
        #         print('excel_count: {}'.format(self.csv_count))
        #         for item in items:
        #             writer.writerow(item)
        #             csvfile.flush()
        #         pass
        #     self.connection.commit()


process = CrawlerProcess({
    # 'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

})
process.crawl(GoogleSpider)
process.start()
# 3beb0b6c427ba2bd3 engine id
# AIzaSyAFeY2Mn9E5DTZX_lgwthkk5HO9qNUpJEQ api
# https://cse.google.com/cse?cx=3beb0b6c427ba2bd3 search