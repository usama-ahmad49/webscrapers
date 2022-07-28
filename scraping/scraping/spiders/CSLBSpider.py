try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver

headers = ['Company', 'Company License', 'Company Location/Address', 'Rep Name', 'Rep Phone', 'Address',
           'HIS Registration']
file = open('CSLBSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=headers)
writer.writeheader()


def input_fuc():
    input_file = open('input_CSLBSpider.csv', 'r')
    list = input_file.read().split('\n')
    input_file.close()
    return list


class cslbspider(scrapy.Spider):
    name = 'cslbspider'

    def start_requests(self):
        input_list = input_fuc()
        for inp in input_list:
            url = 'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/NameSearch.aspx?NextName={}&NextLicNum='.format(
                inp)
            yield scrapy.Request(url=url)

    def parse(self, response):
        Company = response.css('#MainContent_dlMain_lblName_0::text').extract_first().strip()
        Company_License = response.css('#MainContent_dlMain_hlLicense_0 ::text').extract_first()
        nexturl = 'https://www.cslb.ca.gov' + response.css(
            '#MainContent_dlMain_hlLicense_0 ::attr(href)').extract_first()
        yield scrapy.Request(url=nexturl, callback=self.parse_license,
                             meta={'Company': Company, 'Company_License': Company_License})

    def parse_license(self, response):
        Address = ', '.join(response.css('#MainContent_BusInfo ::text').extract()[1:3])
        rep_url = 'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/HISList.aspx?LicNum={}&LicName={}&BlockStartsAt=1'.format(
            response.meta['Company_License'], response.meta['Company'])
        yield scrapy.Request(url=rep_url, callback=self.parse_salesperson, meta={'Company': response.meta['Company'],
                                                                                 'Company_License': response.meta[
                                                                                     'Company_License'],
                                                                                 'Address': Address})

    def parse_salesperson(self, response):
        for resp in response.css('#MainContent_dlHisList a'):
            last_url = 'https://www.cslb.ca.gov' + resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=last_url, callback=self.parse_ind_salesperson,
                                 meta={'Company': response.meta['Company'],
                                       'Company_License': response.meta['Company_License'],
                                       'Address': response.meta['Address']})

        if response.css('#MainContent_pnlPager'):
            driver = webdriver.Firefox()
            driver.get(response.url)
            while True:
                driver.find_element_by_id('MainContent_btnNext').click()
                time.sleep(5)
                ps = scrapy.Selector(text=driver.page_source)
                for resp in ps.css('#MainContent_dlHisList a'):
                    last_url = 'https://www.cslb.ca.gov' + resp.css('::attr(href)').extract_first()
                    yield scrapy.Request(url=last_url, callback=self.parse_ind_salesperson,
                                         meta={'Company': response.meta['Company'],
                                               'Company_License': response.meta['Company_License'],
                                               'Address': response.meta['Address']})
                if not driver.find_element_by_id('MainContent_btnNext').is_enabled():
                    driver.close()
                    break


    def parse_ind_salesperson(self, response):
        item = dict()
        item['Rep Name'] = response.css('#MainContent_HISName::text').extract_first()
        item['Address'] = response.css('#MainContent_Address1::text').extract_first() + ', ' + response.css(
            '#MainContent_CityStateZip::text').extract_first()
        item['Rep Phone'] = response.css('#MainContent_PhoneNumber::text').extract_first()
        item['HIS Registration'] = response.css('#MainContent_HIS_No::text').extract_first()
        item['Company'] = response.meta['Company']
        item['Company License'] = response.meta['Company_License']
        item['Company Location/Address'] = response.meta['Address']
        writer.writerow(item)
        file.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(cslbspider)
process.start()
