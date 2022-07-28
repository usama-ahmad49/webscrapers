from selenium import webdriver
import time
import requests
import scrapy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from AirtableApi import AirtableClient

basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'kmc'
airtable_client = AirtableClient(apikey, basekey)
if __name__ == '__main__':
    processed = []
    url = 'https://eservices.kmc.nsw.gov.au/T1PRProd/WebApps/eProperty/P1/eTrack/eTrackApplicationSearch.aspx?r=KC_WEBGUEST&f=P1.ETR.SEARCH.ENQ'
    driver = webdriver.Chrome()
    driver.get(url)
    datestr1 = '01/01/1950'
    datestr2 = '23/05/2021'
    driver.find_element_by_css_selector('#ctl00_Content_txtDateFrom_txtText').send_keys(datestr1)
    driver.find_element_by_css_selector('#ctl00_Content_txtDateTo_txtText').send_keys(datestr2)
    driver.find_element_by_id('ctl00_Content_btnSearch').click()
    cont = True
    while cont:
        response = scrapy.Selector(text=driver.page_source)
        for resp in response.css('.normalRow,.alternateRow'):
            item = dict()
            item['Application Number'] = resp.css('td:nth-child(1) a::text').extract_first()
            item['Date of application'] = resp.css('td:nth-child(2) ::text').extract_first()
            item['Application Description'] = resp.css('td:nth-child(3) ::text').extract_first()
            item['Property Address'] = resp.css('td:nth-child(6) a::text').extract_first()
            # item['Name of applicant'] = resp.css('td:nth-child(7) ::text').extract_first()
            item['Domain'] = 'kmc.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            processed.append(item)
        if '...' in driver.find_elements_by_css_selector('.pagerRow table tr td')[0].text:
            i = 2
            tot = 11
        else:
            i = 1
            tot = 10
        while i < tot:
            try:
                driver.find_elements_by_css_selector('.pagerRow table tr td')[i].click()
            except:
                driver.find_elements_by_css_selector('.pagerRow table tr td')[i + 1].click()
            i += 1
            try:
                WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_Content_cusResultsGrid_repWebGrid_ctl00_grdWebGridTabularView"]/tbody/tr[17]/td/table/tbody/tr/td[2]')))
            except TimeoutException:
                print('timeout')
            response = scrapy.Selector(text=driver.page_source)
            for resp in response.css('.normalRow,.alternateRow'):
                item = dict()
                item['Application Number'] = resp.css('td:nth-child(1) a::text').extract_first()
                item['Date of application'] = resp.css('td:nth-child(2) ::text').extract_first()
                item['Application Description'] = resp.css('td:nth-child(3) ::text').extract_first()
                item['Property Address'] = resp.css('td:nth-child(6) a::text').extract_first()
                # item['Name of applicant'] = resp.css('td:nth-child(7) ::text').extract_first()
                item['Domain'] = 'blacktown.nsw.gov.au'
                suburb = ''
                for str in resp.css('td:nth-child(6) a::text').extract_first().split():
                    if str.isupper():
                        suburb = suburb + ' ' + str
                item['Suburb'] = suburb
                processed.append(item)
        if '...' in driver.find_elements_by_css_selector('.pagerRow table tr td')[-1].text:
            driver.find_elements_by_css_selector('.pagerRow table tr td')[-1].click()
            try:
                WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_Content_cusResultsGrid_repWebGrid_ctl00_grdWebGridTabularView"]/tbody/tr[17]/td/table/tbody/tr/td[2]')))
            except TimeoutException:
                print('timeout')
        else:
            cont = False
    driver.quit()
    airtable_client.insert_records(table_name, processed)