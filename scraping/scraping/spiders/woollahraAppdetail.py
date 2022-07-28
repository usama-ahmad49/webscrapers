from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import scrapy
from AirtableApi import AirtableClient

baseKey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'woollahra'
airtable_client = AirtableClient(apikey, baseKey)
if __name__ == '__main__':
    processed = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    driver.maximize_window()
    for i in range(0, 4):
        url = 'https://eservices.woollahra.nsw.gov.au/eservice/daEnquiryInit.do?nodeNum=5270'
        driver.get(url)
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/fieldset/fieldset[1]/div[1]/label[4]/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/div/input[1]').click()
        elif i == 1:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/fieldset/fieldset[1]/div[1]/label[5]/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/div/input[1]').click()
        elif i == 2:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/fieldset/fieldset[2]/div[1]/label[4]/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/div/input[1]').click()
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/fieldset/fieldset[2]/div[1]/label[5]/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="daEnquiryForm"]/div/input[1]').click()
        resp = scrapy.Selector(text=driver.page_source)
        for i,r in enumerate(resp.css('#fullcontent div:nth-child(3) h4')):
            item = dict()
            item['Application Number']=resp.css('#fullcontent div:nth-child(3) div')[i].css('p:nth-child(4) .inputField::text').extract_first()
            item['Date of application']=resp.css('#fullcontent div:nth-child(3) div')[i].css('p:nth-child(5) .inputField::text').extract_first()
            item['Application Description']=resp.css('#fullcontent div:nth-child(3) div')[i].css('p:nth-child(1) .inputField::text').extract_first()
            item['Property Address']=r.css('a::text').extract_first()
            # item['Application Status']=''
            item['Domain']='woollahra.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            item['Name of applicant']=resp.css('#fullcontent div:nth-child(3) div')[i].css('p:nth-child(2) .inputField::text').extract_first()
            processed.append(item)
    driver.quit()
    airtable_client.insert_records(table_name, processed)