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

table_name = 'two_Blacktown'
airtable_client = AirtableClient(apikey, basekey)


if __name__ == '__main__':
    processed = []
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = 'https://epathway.thehills.nsw.gov.au/ePathway/Production/Web/Default.aspx'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/div/div/div/div/fieldset/div/span/div[1]/div[6]/a').click()
    try:
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_MainBodyContent_mContinueButton"]')))
    except TimeoutException:
        print('timeout')
    driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mDataList_ctl03_mDataGrid_ctl02_ctl00"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mContinueButton"]').click()
    try:
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mSearchButton"]')))
    except TimeoutException:
        print('timeout')
    driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_tabControlMenun1"]/table/tbody/tr/td/a').click()
    try:
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mDateFromLabel"]')))
    except TimeoutException:
        print('timeout')
    datestr1 = '01/01/1950'
    datestr2 = '17/05/2021'
    driver.find_element_by_id('ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mFromDatePicker_dateTextBox').clear()
    driver.find_element_by_id('ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mFromDatePicker_dateTextBox').send_keys(datestr1)
    driver.find_element_by_id('ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mToDatePicker_dateTextBox').clear()
    driver.find_element_by_id('ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mToDatePicker_dateTextBox').send_keys(datestr2)
    driver.find_element_by_id('ctl00_MainBodyContent_mGeneralEnquirySearchControl_mSearchButton').click()
    try:
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_MainBodyContent_mPagingControl_TableCell4')))
    except TimeoutException:
        print('timeout')
    totalpages = int(driver.find_element_by_id('ctl00_MainBodyContent_mPagingControl_pageNumberLabel').text.split('of')[-1].strip())
    cont = 1
    while cont<totalpages:
        response = scrapy.Selector(text=driver.page_source)
        for resp in response.css('tr.ContentPanel,tr.AlternateContentPanel'):
            item = dict()
            item['Application Number'] = resp.css('td:nth-child(1) a::text').extract_first()
            item['Date of application'] = resp.css('td:nth-child(2) ::text').extract_first()
            item['Application Description'] = resp.css('td:nth-child(3) ::text').extract_first()
            item['Property Address'] = resp.css('td:nth-child(4) ::text').extract_first()
            item['Application Status'] = resp.css('td:nth-child(5) ::text').extract_first()
            item['Domain'] = 'thehills.nsw.gov.au'
            suburb = ''
            for str in resp.css('td:nth-child(4) ::text').extract_first().split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            processed.append(item)
        cont+=1
        driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mPagingControl_nextPageHyperLink"]').click()
    driver.quit()
    airtable_client.insert_records(table_name, processed)
