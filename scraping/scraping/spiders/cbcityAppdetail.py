from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import scrapy
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'cbcity'
airtable_client = AirtableClient(apikey, baseKey)


if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    for i in range(0, 2):
        url = 'https://eplanning.cbcity.nsw.gov.au/ApplicationSearch'
        driver.get(url)
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/form/table/tbody/tr/td[1]/div/ul/li[6]/a').click()
            time.sleep(1)
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/form/table/tbody/tr/td[1]/div/ul/li[7]/a').click()
            time.sleep(1)
        time.sleep(3)
        resp = scrapy.Selector(text=driver.page_source)
        for r in resp.xpath('/html/body/div[2]/form/table/tbody/tr/td[2]/div'):
            item = dict()
            try:
                try:
                    item['Application Number'] = r.css('h4 a::text').extract_first()
                except:
                    pass
                try:
                    item['Date of application'] = r.css(' ::text').extract()[11].replace('\n','').strip()
                except:
                    pass
                try:
                    item['Application Description'] = r.css(' ::text').extract()[2].replace('\n','').replace('   ','')
                except:
                    pass
                try:
                    item['Property Address'] = r.css(' ::text').extract()[4].replace('\n','').replace('   ','')
                except:
                    pass
                try:
                    item['Application Status'] = r.css(' ::text').extract()[14].strip()
                except:
                    pass
                item['Domain'] = 'cbcity.nsw.gov.au'
                suburb = ''
                for str in item['Property Address'].split():
                    if str.isupper():
                        suburb = suburb + ' ' + str
                item['Suburb'] = suburb
                try:
                    item['Name of applicant'] = r.css(' ::text').extract()[23].strip()
                except:
                    pass

                processed.append(item)
            except:
                pass
    driver.quit()
    airtable_client.insert_records(table_name, processed)