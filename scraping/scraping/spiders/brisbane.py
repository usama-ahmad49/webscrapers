import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as ff_options
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import AirtableApi

processed = []
suburbList = []
applicationNumberList = []

basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PADtable'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)
class brisbane(scrapy.Spider):
    name = 'brisbane'

    def start_requests(self):
        url = 'https://www.brisbane.qld.gov.au/about-council/council-information-and-rates/brisbane-suburbs'
        res = requests.get(url=url)
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        for ress in resp.css('.js-table--responsive tbody'):
            for re in ress.css('tr'):
                suburb = re.css('td:nth-child(1)::text').extract_first()
                suburbList.append(suburb)
        options = ff_options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=options)
        driver.get('https://developmenti.brisbane.qld.gov.au/Home/MapSearch')
        inputEl = driver.find_element_by_id('addressLookup')
        for suburb in suburbList[:1]:
            inputEl.send_keys(Keys.CONTROL+'a')
            inputEl.send_keys(Keys.BACK_SPACE)
            inputEl.send_keys(suburb)
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-id-5"]/li[2]/div')))
            except TimeoutException:
                print('timeout')
            driver.find_element_by_xpath('//*[@id="ui-id-5"]/li[2]/div').click()
            try:
                WebDriverWait(driver,25).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#associatedApplications .application-tile.col-md-12.cf')))
            except TimeoutException:
                print('timeout')
            response = scrapy.Selector(text=driver.page_source)
            for res in response.css('#associatedApplications .application-tile.col-md-12.cf'):
                appNum= [res.css('h5::text').extract_first().split(':')[-1].strip(),suburb]
                applicationNumberList.append(appNum)
        driver.quit()
        for appNum in applicationNumberList:
            detailurl = f'https://developmenti.brisbane.qld.gov.au/Home/ApplicationDetail?type=plan_development_apps_unique&id={appNum[0]}'
            yield scrapy.Request(url=detailurl, meta={'suburb':appNum[1]})

    def parse(self, response, **kwargs):
        item = dict()
        item['Application Number'] = ''.join(response.css('.col-sm-12.col-md-8.col-lg-8.details.cf .col-sm-12')[0].css('.col-sm-8 ::text').extract()).strip()
        item['Domain'] = 'developmenti.brisbane.qld.gov.au'
        item['suburb'] = response.meta['suburb']
        timestamp = int(response.css('.col-sm-12.col-md-8.col-lg-8.details.cf .col-sm-12')[7].css('.col-sm-8 span::attr(data-date-number)').extract_first())/1000
        item['Date of application'] = datetime.fromtimestamp(timestamp).strftime('%D')
        item['Name of applicant'] = ''.join(response.css('.col-sm-12.col-md-8.col-lg-8.details.cf .col-md-12')[0].css('.col-sm-8 ::text').extract()).strip().split('-')[-1].split('(Primary Applicant)')[0]
        item['Property Address'] = response.css('.col-md-12.associations .col-md-12 a::text').extract_first()
        item['Application Description'] = ''.join(response.css('.col-sm-12.col-md-8.col-lg-8.details.cf .col-md-12')[0].css('.col-sm-8 ::text').extract()).strip()
        item['Application Status'] = ''.join(response.css('.col-sm-12.col-md-8.col-lg-8.details.cf .col-sm-12')[1].css('.col-sm-8 ::text').extract()).strip()

        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(brisbane)
process.start()
