from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import scrapy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'northSydney'
airtable_client = AirtableClient(apikey, baseKey)


if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    for i in range(0, 4):
        url = 'https://apptracking.northsydney.nsw.gov.au/Pages/XC.Track/SearchApplication.aspx'
        driver.get(url)
        try:
            driver.find_element_by_id('ctl00_ctMain_BtnAgree').click()
        except:
            pass
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="m10037"]').click()
            time.sleep(1)
            driver.find_element_by_css_selector('.level-2.no-child.i10037.ii10041 a').click()
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="m10037"]').click()
            time.sleep(1)
            driver.find_element_by_css_selector('.level-2.no-child.i10037.ii10040 a').click()
        elif i == 2:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="m10042"]').click()
            time.sleep(1)
            driver.find_element_by_css_selector('.level-2.no-child.i10042.ii10046 a').click()
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="m10042"]').click()
            time.sleep(1)
            driver.find_element_by_css_selector('.level-2.no-child.i10042.ii10045 a').click()
        time.sleep(3)
        resp = scrapy.Selector(text=driver.page_source)
        for r in resp.css('#hiddenresult tr'):
            item = dict()
            ind_link ='https://apptracking.northsydney.nsw.gov.au/'+ r.css('a::attr(href)').extract_first().split('../')[-1]
            item['Application Number'] = r.css('td:nth-child(2) strong::text').extract_first()
            item['Date of application'] = r.css('td:nth-child(3)::text').extract_first()
            item['Application Description'] = ''.join(r.css('td:nth-child(4)::text').extract()).strip()
            item['Property Address'] = r.css('td:nth-child(4) strong::text').extract_first()
            # item['Application Status'] = r.css('td:nth-child(5) ::text').extract_first()
            item['Domain'] = 'northsydney.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            driver.get(ind_link)
            newResp = scrapy.Selector(text=driver.page_source)
            item['Name of applicant'] = ''.join(newResp.css('#b_ctl00_ctMain_info_party::text').extract()).replace('Applicant', '').replace('\n', ' ;').replace('    ', '').replace('-', '')
            try:
                item['Application Status'] = newResp.css('#b_ctl00_ctMain_info_det ::text').extract_first()
            except:
                pass

            processed.append(item)

    driver.quit()
    airtable_client.insert_records(table_name, processed)