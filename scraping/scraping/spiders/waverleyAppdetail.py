from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import scrapy
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'waverley'
airtable_client = AirtableClient(apikey, baseKey)


if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    driver.maximize_window()
    for i in range(0, 4):
        url = 'https://eservices.waverley.nsw.gov.au/pages/xc.track/searchapplication.aspx'
        driver.get(url)
        try:
            driver.find_element_by_id('ctl00_ctMain_BtnAgree').click()
        except:
            pass
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="l10401"]/a').click()
            time.sleep(1)
            driver.find_element_by_css_selector('#l10360 a').click()
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="l10401"]/a').click()
            time.sleep(1)
            driver.find_element_by_css_selector('#l10361 a').click()
        elif i == 2:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="l10402"]/a').click()
            time.sleep(1)
            driver.find_element_by_css_selector('#l10364 a').click()
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="l10402"]/a').click()
            time.sleep(1)
            driver.find_element_by_css_selector('#l10365 a').click()
        time.sleep(3)
        resp = scrapy.Selector(text=driver.page_source)
        for r in resp.css('#hiddenresult .result'):
            item = dict()
            ind_link ='https://eservices.waverley.nsw.gov.au/'+ r.css('a::attr(href)').extract_first().split('../')[-1]
            driver.get(ind_link)
            newResp = scrapy.Selector(text=driver.page_source)
            item['Application Number'] = newResp.css('.detailHeading::text').extract_first().split(':')[-1].strip()
            item['Date of application'] = ''.join(newResp.css('#ctl00_ctMain_info_pnlApplication > div:nth-child(2) > div.detail > div.detailright ::text').extract()).split('\n')[3].split(':')[-1].strip()
            item['Application Description'] = ''.join(newResp.css('#ctl00_ctMain_info_pnlApplication > div:nth-child(2) > div.detail > div.detailright ::text').extract()).split('\n')[0].replace('   ','')
            item['Property Address'] = ''.join(newResp.css('#b_ctl00_ctMain_info_prop .detailright ::text').extract()).replace('\n','').strip()
            item['Application Status'] = ''.join(newResp.css('#ctl00_ctMain_info_pnlApplication > div:nth-child(2) > div.detail > div.detailright ::text').extract()).split('\n')[2].strip()
            item['Domain'] = 'waverley.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            try:
                item['Name of applicant'] = newResp.css('#b_ctl00_ctMain_info_party .detailright::text').extract_first().split('-')[-1]
            except:
                pass

            processed.append(item)
    driver.quit()
    airtable_client.insert_records(table_name, processed)