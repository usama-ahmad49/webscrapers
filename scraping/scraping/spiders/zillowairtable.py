import json

import scrapy
from scrapy.crawler import CrawlerProcess

import AirtableApi

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

Processed = []
table_name = 'zillow'
basekey = 'appctQUT8ZpjYyfIJ'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'
airtable_client = AirtableApi.AirtableClient(apikey, basekey)


class zillowairtable(scrapy.Spider):
    name = 'zillowairtable'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'e966c8ccb90048c5918621698013e2fc',
        'CONCURRENT_REQUESTS': 32,
        'AUTOTHROTTLE_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        'DOWNLOAD_TIMEOUT': 600,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408]
    }

    def start_requests(self):
        IndividualLinks = []
        Rfile = open('input_zillow.txt', 'r')
        inputfile = Rfile.read()
        links = inputfile.split('\n')
        links = [z for z in links if z.strip()]

        for link in links[40:]:
            url = f'https://www.zillow.com/homes/{link}_rb/'
            yield scrapy.Request(url=url)
            # driver = ie.Ie ()
            # driver.maximize_window ()
            # while True :
            #     try :
            #         driver.get ( url=url )
            #         break
            #     except TimeoutException :
            #         print ( 'timeout' )
            # time.sleep ( 5 )
            # while True :
            #     # wait for captcha solve
            #     if 'https://www.zillow.com/captchaPerimeterX/' in driver.current_url :
            #         winsound.Beep ( 500, 1000 )
            #         driver.quit ()
            #         time.sleep ( 120 )
            #         driver = ie.Ie ()
            #         while True :
            #             try :
            #                 driver.get ( url )
            #                 break
            #             except TimeoutException :
            #                 print ( 'timeout' )
            #         time.sleep ( 5 )
            #     else :
            #         break
            # print ( 'this' )
            # driver.execute_script ( "arguments[0].scrollIntoView();", driver.find_element_by_css_selector ( 'footer' ) )
            #
            # while True :
            #     try :
            #         if driver.find_element_by_css_selector ( 'a[title="Next page"]' ).get_attribute (
            #                 'tabindex' ) != None :
            #             response = scrapy.Selector ( text=driver.page_source )
            #             for res in response.css (
            #                     '#grid-search-results .photo-cards.photo-cards_wow.photo-cards_short.photo-cards_extra-attribution li' ) :
            #                 if 'nav-ad-container' in res.css ( 'div::attr(id)' ) :
            #                     continue
            #                 if res.css ( '.list-card-info a::attr(href)' ).extract_first () == None :
            #                     continue
            #                 if res.css ( '.list-card-info a::attr(href)' ).extract_first () not in IndividualLinks :
            #                     IndividualLinks.append ( res.css ( '.list-card-info a::attr(href)' ).extract_first () )
            #             break
            #     except :
            #         response = scrapy.Selector ( text=driver.page_source )
            #         for res in response.css (
            #                 '#grid-search-results .photo-cards.photo-cards_wow.photo-cards_short.photo-cards_extra-attribution li' ) :
            #             if 'nav-ad-container' in res.css ( 'div::attr(id)' ) :
            #                 continue
            #             if res.css ( '.list-card-info a::attr(href)' ).extract_first () == None :
            #                 continue
            #             if res.css ( '.list-card-info a::attr(href)' ).extract_first () not in IndividualLinks :
            #                 IndividualLinks.append ( res.css ( '.list-card-info a::attr(href)' ).extract_first () )
            #         break
            #     response = scrapy.Selector ( text=driver.page_source )
            #     for res in response.css (
            #             '#grid-search-results .photo-cards.photo-cards_wow.photo-cards_short.photo-cards_extra-attribution li' ) :
            #         if 'nav-ad-container' in res.css ( 'div::attr(id)' ) :
            #             continue
            #         if res.css ( '.list-card-info a::attr(href)' ).extract_first () == None :
            #             continue
            #         if res.css ( '.list-card-info a::attr(href)' ).extract_first () not in IndividualLinks :
            #             IndividualLinks.append ( res.css ( '.list-card-info a::attr(href)' ).extract_first () )
            #
            #     driver.execute_script ( "arguments[0].scrollIntoView();",
            #                             driver.find_element_by_css_selector ( 'footer' ) )
            #     try :
            #         currentUrl = driver.current_url
            #         driver.find_element_by_css_selector ( 'a[title="Next page"]' ).click ()
            #     except :
            #         break
            #     time.sleep ( 4 )
            #     while True :
            #         # wait for captcha solve
            #         if 'https://www.zillow.com/captchaPerimeterX/' in driver.current_url :
            #             winsound.Beep ( 500, 1000 )
            #             driver.quit ()
            #             time.sleep ( 120 )
            #             driver = ie.Ie ()
            #             while True :
            #                 try :
            #                     driver.get ( currentUrl )
            #                     break
            #                 except TimeoutException :
            #                     print ( 'timeout' )
            #             time.sleep ( 5 )
            #         else :
            #             break
            # driver.quit ()
            # for url in IndividualLinks :
            #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        data = (json.loads([v for v in response.css('script[type="application/json"]::text').extract() if 'queryState' in v][0].replace('<!--', '').replace('-->', '')))['cat1']['searchResults']['listResults']
        for link in data:
            yield scrapy.Request(url=link['detailUrl'], callback=self.parse_data, meta={'zpid': link['zpid']})

    def parse_data(self, response):
        item = dict()
        item['link'] = response.url
        zpid = response.meta['zpid']
        try:
            areacode = str(json.loads(
                json.loads(response.css('#hdpApolloPreloadedData::text').extract_first())['apiCache'])[
                               'ForSaleDoubleScrollFullRenderQuery{"zpid":' + zpid + ',"contactFormRenderParameter":{"zpid":' + zpid + ',"platform":"desktop","isDoubleScroll":true}}'][
                               'property']['contactFormRenderData']['data']['contact_recipients'][0]['phone'][
                               'areacode'])
        except:
            areacode = ''
        try:
            prefix = str(json.loads(
                json.loads(response.css('#hdpApolloPreloadedData::text').extract_first())['apiCache'])[
                             'ForSaleDoubleScrollFullRenderQuery{"zpid":' + zpid + ',"contactFormRenderParameter":{"zpid":' + zpid + ',"platform":"desktop","isDoubleScroll":true}}'][
                             'property']['contactFormRenderData']['data']['contact_recipients'][0]['phone'][
                             'prefix'])
        except:
            prefix = ''
        try:
            number = str(json.loads(
                json.loads(response.css('#hdpApolloPreloadedData::text').extract_first())['apiCache'])[
                             'ForSaleDoubleScrollFullRenderQuery{"zpid":' + zpid + ',"contactFormRenderParameter":{"zpid":' + zpid + ',"platform":"desktop","isDoubleScroll":true}}'][
                             'property']['contactFormRenderData']['data']['contact_recipients'][0]['phone'][
                             'number'])
        except:
            number = ''
        item['Phone'] = areacode + prefix + number
        if item['Phone'] == '' or None:
            return

        propertydetails = json.loads(
            json.loads(response.css('#hdpApolloPreloadedData::text').extract_first())['apiCache'])[
            'ForSaleDoubleScrollFullRenderQuery{"zpid":' + zpid + ',"contactFormRenderParameter":{"zpid":' + zpid + ',"platform":"desktop","isDoubleScroll":true}}'][
            'property']
        try:
            item['address'] = propertydetails['address']['streetAddress'] + ', ' + propertydetails['address'][
                'city'] + ', ' + propertydetails['address']['state'] + ', ' + propertydetails['address']['zipcode']
        except:
            pass
        try:
            item['price'] = str(propertydetails['price'])
        except:
            pass
        try:
            item['picture'] = [{"url": propertydetails['tourPhotos'][0]['url']}]
        except:
            pass
        try:
            item['beds'] = str(propertydetails['bedrooms'])
        except:
            pass
        try:
            item['baths'] = str(propertydetails['bathrooms'])
        except:
            pass
        try:
            item['sqft'] = str(propertydetails['resoFacts']['livingArea'])
        except:
            pass
        try:
            item['status'] = propertydetails['homeStatus']
        except:
            pass
        try:
            item['zestimate'] = str(propertydetails['zestimate'])
        except:
            pass
        try:
            item['Year built'] = str(propertydetails['yearBuilt'])
        except:
            pass
        try:
            item['LotSize'] = str(propertydetails['lotSize'])
        except:
            pass

        Processed.append(item)
        firstcol = 'link'
        airtable_client.insert_records(table_name, Processed, firstcol)
        Processed.clear()


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(zillowairtable)
process.start()
