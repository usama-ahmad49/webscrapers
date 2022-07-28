from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import scrapy
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'willough'
airtable_client = AirtableClient(apikey, baseKey)
if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    for i in range(0, 4):
        url = 'https://eplanning.willoughby.nsw.gov.au/pages/xc.track/searchapplication.aspx'
        driver.get(url)
        time.sleep(3)
        try:
            driver.find_element_by_id('ctl00_ctMain_chkAgree_chk1').click()
        except:
            pass
        time.sleep(0.5)
        try:
            driver.find_element_by_id('ctl00_ctMain_BtnAgree').click()
        except:
            pass
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i4"]/a[3]').click()
            time.sleep(1)
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i4"]/a[4]').click()
            time.sleep(1)
        elif i == 2:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i5"]/a[3]').click()
            time.sleep(1)
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i5"]/a[4]').click()
            time.sleep(1)
        resp = scrapy.Selector(text=driver.page_source)
        for r in resp.css('#hiddenresult .result'):
            item = dict()
            ind_link = 'https://eplanning.willoughby.nsw.gov.au/' + r.css('a::attr(href)').extract_first().split('../')[-1]
            driver.get(ind_link)
            newResp = scrapy.Selector(text=driver.page_source)
            try:
                item['Application Number'] = newResp.css('#ctl00_ctMain_info_pnlApplication h2::text').extract_first().strip()
            except:
                pass
            try:
                item['Date of application'] = newResp.css('#b_ctl00_ctMain_info_app table tr')[1].css('td:nth-child(2)::text').extract_first()
            except:
                pass
            try:
                item['Application Description'] = ''.join(newResp.css('#b_ctl00_ctMain_info_app::text').extract()).replace('\n','').strip()
            except:
                pass
            try:
                item['Property Address'] = newResp.css('#ctl00_ctMain_info_pnlApplication h3::text').extract_first().replace('\n',' ')
            except:
                pass
            try:
                item['Application Status'] = newResp.css('#b_ctl00_ctMain_info_app table tr td strong::text').extract_first()
            except:
                pass
            item['Domain'] = 'willoughby.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            try:
                item['Name of applicant'] = newResp.css('#b_ctl00_ctMain_info_party::text').extract_first().split('-')[-1].replace('\n','').strip()
            except:
                pass

            processed.append(item)
    driver.quit()
    airtable_client.insert_records(table_name, processed)