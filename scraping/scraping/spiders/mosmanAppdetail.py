from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import scrapy
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'mosman'
airtable_client = AirtableClient(apikey, baseKey)


if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    for i in range(0, 4):
        url = 'https://portal.mosman.nsw.gov.au/pages/xc.track/SearchProperty.aspx'
        driver.get(url)
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i10650"]/a[3]').click()
            time.sleep(1)
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i10650"]/a[4]').click()
            time.sleep(1)
        elif i == 2:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i10655"]/a[3]').click()
            time.sleep(1)
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i10655"]/a[4]').click()
            time.sleep(1)
        time.sleep(3)
        resp = scrapy.Selector(text=driver.page_source)
        for r in resp.css('#hiddenresult .result'):
            item = dict()
            ind_link ='https://portal.mosman.nsw.gov.au/pages/xc.track/'+ r.css('a::attr(href)').extract_first().split('../')[-1]
            driver.get(ind_link)
            newResp = scrapy.Selector(text=driver.page_source)
            try:
                item['Application Number'] = newResp.css('#ctl00_ctMain_info_pnlApplication table h2::text').extract_first().split(':')[-1].strip()
            except:
                pass
            try:
                item['Date of application'] = newResp.css('#ctl00_ctMain_info_pnlApplication .ndetail')[1].css('.ndetailright::text').extract_first()
            except:
                pass
            try:
                item['Application Description'] = newResp.css('#ctl00_ctMain_info_pnlApplication .ndetail')[0].css('.ndetailright::text').extract_first()
            except:
                pass
            try:
                item['Property Address'] = newResp.css('#ctl00_ctMain_info_pnlApplication #addr a::text').extract_first().strip()
            except:
                pass
            try:
                item['Application Status'] = newResp.css('#ctl00_ctMain_info_pnlApplication .ndetail')[2].css('.ndetailright::text').extract_first().strip()
            except:
                pass
            item['Domain'] = 'mosman.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            # try:
            #     item['Name of applicant'] = newResp.css('#b_ctl00_ctMain_info_party .detailright::text').extract_first().split('-')[-1]
            # except:
            #     pass

            processed.append(item)
    driver.quit()
    airtable_client.insert_records(table_name, processed)