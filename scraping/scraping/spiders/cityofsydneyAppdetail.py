import time
import json
import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'kmc'
airtable_client = AirtableClient(apikey, basekey)
processed = []

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
    "Accept": "*/*",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://online2.cityofsydney.nsw.gov.au",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://online2.cityofsydney.nsw.gov.au/DA/SearchResult",
    "Accept-Language": "en-US,en;q=0.9"
}

cookies = {
    "_hjTLDTest": "1",
    "_hjid": "2ef4621f-49ea-4626-bf1e-82560a3edb76",
    "_fbp": "fb.2.1621248778249.970270665",
    "nmstat": "8dd3a5b7-7d6d-476f-b181-289e9154f52f",
    "ASP.NET_SessionId": "1nirl40pxw1fzxryeqboelnj",
    "__RequestVerificationToken": "oeFyREurvCgJ0EegITYr5hDg9mGgJFrNf6_4QrXXbQXmy3kaqk0L277qjFOImUGEcbXDLkY-bh8lPwuBKsMyZ7zxLC888ETg3kPY2P3YZXSOcpO5tz0b5wajBkKY3IReVXIR2g2",
    "_gid": "GA1.3.1709857106.1621831387",
    "_ga_XQTKNZ0JEV": "GS1.1.1621837818.3.0.1621837818.60",
    "_ga_73LEPVVGXQ": "GS1.1.1621939394.8.1.1621939395.59",
    "_ga": "GA1.3.850840895.1621237447"
}

body = '__RequestVerificationToken=mTgS0NxufRa5w0vrZBsyfgcBDd6PV9zBVGsCygndWqX3x77WmXK7C5E_r_BCjYEQvhlqWPuGk7BGIWWrPby5fcVM6StMYqYO4NzkvvQlqLjOoc_QumUMGWYsuigT1bMSDzk1UQ2&PageSize=100&CurrentPage=1&SelectedCriteria=Address&Address=&Street=&SelectedCriteriaSuburb=&App_Number=&App_Year=&DateSearchOn=Lodged&DayRange=AllDates&FromDate=&ToDate=&SelectedSuburb=ALEXANDRIA%2CANNANDALE%2CBARANGAROO%2CBEACONSFIELD%2CCAMPERDOWN%2CCENTENNIAL+PARK%2CCHIPPENDALE%2CDARLINGHURST%2CDARLINGTON%2CDAWES+POINT%2CELIZABETH+BAY%2CERSKINEVILLE%2CEVELEIGH%2CFOREST+LODGE%2CGLEBE%2CHAYMARKET%2CMILLERS+POINT%2CMOORE+PARK%2CNEWTOWN%2CPADDINGTON%2CPOTTS+POINT%2CPYRMONT%2CREDFERN%2CROSEBERY%2CRUSHCUTTERS+BAY%2CST+PETERS%2CSURRY+HILLS%2CSYDNEY%2CTHE+ROCKS%2CULTIMO%2CWATERLOO%2CWOOLLOOMOOLOO%2CZETLAND&SelectedApplicationType=Development+Applications%2CFootway+Usage+Application+-+Outdoor+Dining&SelectedExhibition=1%2C2%2C0&Tpklpaprops=&IncludeAdjoining=False'

class cityofsydneyAppdetail(scrapy.Spider):
    name = 'cityofsydneyAppdetail'

    def start_requests(self):
        url = 'https://online2.cityofsydney.nsw.gov.au/DA/GridPagination/'
        yield scrapy.Request(url=url, method='POST', headers=headers, cookies=cookies, body=body)
    def parse(self, response, **kwargs):
        jsondata = json.loads(response.text)
        html = jsondata['dataGrid2PartialView']
        resp = scrapy.Selector(text=html)
        total_pages = int(resp.css('#TotalPage::attr(value)').extract_first())
        i=0
        while i<=2:
            i+=1
            body_2 = f'__RequestVerificationToken=mTgS0NxufRa5w0vrZBsyfgcBDd6PV9zBVGsCygndWqX3x77WmXK7C5E_r_BCjYEQvhlqWPuGk7BGIWWrPby5fcVM6StMYqYO4NzkvvQlqLjOoc_QumUMGWYsuigT1bMSDzk1UQ2&PageSize=100&CurrentPage={i}&SelectedCriteria=Address&Address=&Street=&SelectedCriteriaSuburb=&App_Number=&App_Year=&DateSearchOn=Lodged&DayRange=AllDates&FromDate=&ToDate=&SelectedSuburb=ALEXANDRIA%2CANNANDALE%2CBARANGAROO%2CBEACONSFIELD%2CCAMPERDOWN%2CCENTENNIAL+PARK%2CCHIPPENDALE%2CDARLINGHURST%2CDARLINGTON%2CDAWES+POINT%2CELIZABETH+BAY%2CERSKINEVILLE%2CEVELEIGH%2CFOREST+LODGE%2CGLEBE%2CHAYMARKET%2CMILLERS+POINT%2CMOORE+PARK%2CNEWTOWN%2CPADDINGTON%2CPOTTS+POINT%2CPYRMONT%2CREDFERN%2CROSEBERY%2CRUSHCUTTERS+BAY%2CST+PETERS%2CSURRY+HILLS%2CSYDNEY%2CTHE+ROCKS%2CULTIMO%2CWATERLOO%2CWOOLLOOMOOLOO%2CZETLAND&SelectedApplicationType=Development+Applications%2CFootway+Usage+Application+-+Outdoor+Dining&SelectedExhibition=1%2C2%2C0&Tpklpaprops=&IncludeAdjoining=False'
            yield scrapy.Request(url=response.url, method='POST', dont_filter=True,headers=headers, cookies=cookies, body=body_2, callback=self.parsedata)
    def parsedata(self,response):
        jsondata = json.loads(response.text)
        html = jsondata['dataGrid2PartialView']
        resp = scrapy.Selector(text=html)
        for re in resp.css('table.bottomBorder tr')[1:]:
            item = dict()
            item['Application Number'] =re.css('.developmentApplications::text').extract_first()
            item['Date of application'] =re.css('td:nth-child(4)::text').extract_first().strip()
            item['Application Description'] =re.css('td:nth-child(3) span::text').extract_first()
            item['Property Address'] =re.css('td:nth-child(2)::text').extract_first().strip().replace('\r','')
            # item['Name of applicant'] ='
            item['Domain'] = 'cityofsydney.nsw.gov.au'
            suburb = ''
            for str in item['Property Address'].split():
                if str.isupper():
                    suburb = suburb + ' ' + str
            item['Suburb'] = suburb
            processed.append(item)
    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(cityofsydneyAppdetail)
process.start()