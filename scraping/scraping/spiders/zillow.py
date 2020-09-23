import json
import time

import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options as ff_options
#from scraping import settings


Rfile=open('zipcode_zillow.txt','r')
inputfile=Rfile.read()

Wfile=open('zillowData.csv','w',encoding='utf-8',newline='')
csv_columns=['Price','Bedrooms','Bathrooms','Square feet','Address','Listing type','Zestimate','Est. payment:','Time on Zillow','Type:','Year built:','Heating:','Cooling:','Parking:','HOA:','Lot:','Price/sqft:','Rent Zestimate','Neighborhood stats','median Zestimate','Zillow link',]
writer=csv.DictWriter(Wfile,fieldnames=csv_columns)
writer.writeheader()

options = ff_options()
options.add_argument('--headless')
driver = webdriver.Firefox(firefox_options=options)


class zillow(scrapy.Spider):

    name = 'zillow'
    template_url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{}%7D%2C%22usersSearchTerm%22%3A%22{}%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.08536545581086%2C%22east%22%3A-73.9504396135257%2C%22south%22%3A40.69677215592377%2C%22north%22%3A40.77733747707232%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A61615%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketPreForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22,%22total%22]}&requestId={}'
    request_count = 1

    def close_driver(cls, driver):
        driver.quit()

    def start_requests(self):

        new_url = 'https://www.zillow.com/homes/10001_rb/'
        yield scrapy.Request(new_url, meta={'url':new_url})

    def parse(self, responce):
        inputdata=inputfile.split('\n')
        for input in inputdata:
            url='https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%22'+str(input)+'%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.08536545581086%2C%22east%22%3A-73.9504396135257%2C%22south%22%3A40.69677215592377%2C%22north%22%3A40.77733747707232%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A61615%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketPreForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22,%22total%22]}&requestId=2'
            yield scrapy.Request(url,self.parse_23, meta={'input':input})






    def parse_23(self, response):
        dataforpage = json.loads(response.body)
        pageno = dataforpage.get('cat1', {}).get('searchList', {}).get('totalPages')

        i=1
        while i<=pageno:
            page=('{}_p').format(i)
            i=i+1
            url=('https://www.zillow.com/homes/{}_rb/{}').format(response.meta['input'],page)

            driver.get(url)
            time.sleep(5)
            requests_data = [r for r in driver.requests if 'pagination%22%3A%7B%7D%2C%22usersSearchTerm' in r.path]
            data = json.loads(requests_data[0].response.body)
            if(len(data)==11):
                for zillow_property in data.get('searchResults',{}).get('mapResults',{}):
                    item = dict()
                    if (zillow_property.get('buildingId')):
                        item['Zillow link'] = 'https://www.zillow.com{}'.format(zillow_property.get('detailUrl'))
                        item['Price'] = zillow_property.get('price')
                        item['Zestimate'] = 'not available'
                        item['Address'] = zillow_property.get('statusText')
                        item['Bedrooms'] = zillow_property.get('minBeds')
                        item['Bathrooms'] = zillow_property.get('minBaths')
                        item['Square feet'] = zillow_property.get('minArea')
                        item['Listing type'] = zillow_property.get('statusType')
                    else:
                        item['Zillow link'] = 'https://www.zillow.com{}'.format(zillow_property.get('detailUrl'))
                        item['Price'] = zillow_property.get('price')
                        item['Zestimate'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('zestimate')
                        item['Address'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('streetAddress')
                        item['Bedrooms'] = zillow_property.get('beds')
                        item['Bathrooms'] = zillow_property.get('baths')
                        item['Square feet'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('livingArea')
                        item['Listing type'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('homeStatus')
                    writer.writerow(item)
                    #Wfile.flush()
                    print(item)
            else:
                for zillow_property in data.get('cat1',{}).get('searchResults',{}).get('mapResults',{}):
                    item1 = dict()
                    if(zillow_property.get('buildingId')):
                        item1['Zillow link'] = 'https://www.zillow.com{}'.format(zillow_property.get('detailUrl'))
                        item1['Price'] = zillow_property.get('price')
                        item1['Zestimate']='not available'
                        item1['Address']=zillow_property.get('address')
                        item1['Bedrooms']= zillow_property.get('minBeds')
                        item1['Bathrooms']= zillow_property.get('minBaths')
                        item1['Square feet'] = zillow_property.get('minArea')
                        item1['Listing type'] = zillow_property.get('statusType')
                    else:
                        item1['Zillow link'] = 'https://www.zillow.com{}'.format(zillow_property.get('detailUrl'))
                        item1['Price'] = zillow_property.get('price')
                        item1['Zestimate'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('zestimate')
                        item1['Address'] = zillow_property.get('hdpData',{}).get('homeInfo',{}).get('city') +','+zillow_property.get('hdpData',{}).get('homeInfo',{}).get('state')
                        item1['Bedrooms'] = zillow_property.get('beds')
                        item1['Bathrooms'] = zillow_property.get('baths')
                        item1['Square feet'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('livingArea')
                        item1['Listing type'] = zillow_property.get('hdpData', {}).get('homeInfo', {}).get('homeStatus')
                    writer.writerow(item1)
                    #Wfile.flush()
                    print(item1)



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(zillow)
process.start()
