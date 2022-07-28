import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
from scrapy.crawler import CrawlerProcess
now = datetime.today()
now = datetime.strftime(now, '%d/%m/%Y')

import AirtableApi

Processed = []
table_name = 'whittlesea'
basekey = 'appF5JU1xjzYCHQLL'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'
airtable_client = AirtableApi.AirtableClient(apikey, basekey)

if __name__ == '__main__':
    url = 'https://eservice.whittlesea.vic.gov.au/eservice/daEnquiryInit.do?doc_typ=5&nodeNum=21161'
    driver = webdriver.Firefox()
    for i in range(2):
        if i == 0:
            driver.get(url)
            time.sleep(0.5)
            driver.find_element_by_css_selector('#DADateFrom').send_keys('01/01/1960')
            time.sleep(0.5)
            driver.find_element_by_css_selector('#DADateTo').send_keys(now)
            time.sleep(0.5)
        else:
            driver.get(url)
            time.sleep(0.5)
            driver.find_element_by_css_selector('#detDateFromString').send_keys('01/01/1960')
            time.sleep(0.5)
            driver.find_element_by_css_selector('#detDateToString').send_keys(now)
            time.sleep(0.5)
        driver.find_element_by_css_selector('.button.btn.btn-primary').click()
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#daEnquiry_daEnquiryResults')))
        response = scrapy.Selector(text= driver.page_source)
        for i, res in enumerate(response.css('h4.non_table_headers')):
            if response.css('#fullcontent > div:nth-child(3) > div')[i].css('p').__len__() > 5:
                item = dict()
                for res in response.css('#fullcontent > div:nth-child(3) > div')[i].css('p'):
                    item[res.css('.key::text').extract_first()] = res.css('.inputField::text').extract_first()
                Processed.append(item)
            else:
                item = dict()
                item['Application No.'] = response.css('#fullcontent > div:nth-child(3) > div')[i].css('p:nth-child(1) .inputField::text').extract_first()
                item['Address'] = res.css('a::text').extract_first('')
                item['Date Lodged'] = response.css('#fullcontent > div:nth-child(3) > div')[i].css('p:nth-child(2) .inputField::text').extract_first()
                item['Cost of Work'] = response.css('#fullcontent > div:nth-child(3) > div')[i].css('p:nth-child(3) .inputField::text').extract_first()
                item['Determination Details'] = response.css('#fullcontent > div:nth-child(3) > div')[i].css('p:nth-child(4) .inputField::text').extract_first()
                item['Determination Date'] = response.css('#fullcontent > div:nth-child(3) > div')[i].css('p:nth-child(5) .inputField::text').extract_first()
                Processed.append(item)
    driver.quit()
    firstcol = 'Application No.'
    airtable_client.insert_records(table_name, Processed, firstcol)
    print('Done')