import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.firefox.options import Options as ff_options
from seleniumwire import webdriver

import AirtableApi

processed = []
suburbList = []
linkList = []
basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PADtable'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)



class goldcoast(scrapy.Spider):
    name = 'goldcoast'

    def start_requests(self):
        global headers, cookie
        cookie = dict()
        subUrl = 'https://en.wikipedia.org/wiki/List_of_Gold_Coast_suburbs'
        respo = requests.get(url=subUrl)
        resp = scrapy.Selector(text=respo.content.decode('utf-8'))
        for res in resp.css('#mw-content-text div.mw-parser-output table tbody')[1].css('tr')[2:]:
            suburbList.append(res.css('td a::text').extract_first())
        options = ff_options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=options)
        driver.get('https://cogc.cloud.infor.com/ePathway/ePthProd/web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP')
        driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mDataList_ctl03_mDataGrid_ctl04_ctl00"]').click()
        driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mContinueButton"]').click()
        for i, subarb in enumerate(suburbList):
            driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_tabControlMenun1"]/table/tbody/tr/td').click()
            driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl09_mSuburbTextBox"]').send_keys(subarb)
            driver.find_element_by_xpath('//*[@id="ctl00_MainBodyContent_mGeneralEnquirySearchControl_mSearchButton"]').click()
            response = scrapy.Selector(text=driver.page_source)
            gotpagination = False
            if response.css('#ctl00_MainBodyContent_mPagingControl_nextPageHyperLink'):
                gotpagination = True
            for res in response.css('table.ContentPanel tr')[1:]:
                link = ['https://cogc.cloud.infor.com/ePathway/epthprod/Web/GeneralEnquiry/' + res.css('td div a::attr(href)').extract_first(), subarb]
                linkList.append(link)
            while gotpagination:
                driver.find_element_by_id('ctl00_MainBodyContent_mPagingControl_nextPageHyperLink').click()
                response = scrapy.Selector(text=driver.page_source)
                for res in response.css('table.ContentPanel tr')[1:]:
                    link = ['https://cogc.cloud.infor.com/ePathway/epthprod/Web/GeneralEnquiry/' + res.css('td div a::attr(href)').extract_first(), subarb]
                    linkList.append(link)
                if not response.css('#ctl00_MainBodyContent_mPagingControl_nextPageHyperLink'):
                    gotpagination = False
            if i == 0:
                driver.find_element_by_css_selector('tr.ContentPanel:nth-child(2) > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)').click()
                headers = dict([v for v in driver.requests if 'https://cogc.cloud.infor.com/ePathway/epthprod/Web/GeneralEnquiry/EnquiryDetailView.aspx?Id=' in v.url][0].headers)
                del (headers['Cookie'])
                del (headers['Accept-Encoding'])
                for i, v in enumerate(driver.get_cookies()):
                    cookie[v['name']] = v['value']
                del(cookie['_gat'])
            driver.find_element_by_id('ctl00_MainBodyContent_mSearchButton').click()
        driver.quit()

        for link in linkList:
            yield scrapy.Request(url=link[0], method='GET', dont_filter=True, cookies= cookie, headers=headers, meta={'subarb': link[1]})

    def parse(self, response, **kwargs):
        item = dict()
        item['Application Number'] = response.css('#ctl00_MainBodyContent_group_582 .fields .field')[0].css('div::text').extract_first()
        item['Domain'] = 'https://www.goldcoast.qld.gov.au/'
        item['Suburb'] = response.meta['subarb']
        item['Date of application'] = response.css('#ctl00_MainBodyContent_group_582 .fields .field')[3].css('div::text').extract_first()
        item['Name of applicant'] = ''
        item['Property Address'] = response.css('#ctl00_MainBodyContent_group_582 .fields .field')[4].css('div::text').extract_first()
        item['Application Description'] = response.css('#ctl00_MainBodyContent_group_582 .fields .field')[1].css('div::text').extract_first()
        item['Application Status'] = response.css('#ctl00_MainBodyContent_group_582 .fields .field')[5].css('div::text').extract_first()

        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(goldcoast)
process.start()
