try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import json

import AirtableApi
import scrapy
from scrapy.crawler import CrawlerProcess

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)
processed = []


class atrealty(scrapy.Spider):
    name = 'atrealty'

    def start_requests(self):
        urlsale = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=residential&price_type=sale'
        yield scrapy.Request(url=urlsale, meta={'listingtype': 'sale'})
        urlrent = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=residential&price_type=rent'
        yield scrapy.Request(url=urlrent, meta={'listingtype': 'rent'})
        urlcommercialbuy = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=commercial&price_type=sale'
        yield scrapy.Request(url=urlcommercialbuy, meta={'listingtype': 'commercial sale'})
        urlcommercialrent = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=commercial&price_type=rent'
        yield scrapy.Request(url=urlcommercialrent, meta={'listingtype': 'commercial rent'})
        urlbusinesssale = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=residential&price_type=sale'
        yield scrapy.Request(url=urlbusinesssale, meta={'listingtype': 'business sale'})
        urlbusinessrent = 'https://www.atrealty.com.au/wp-json/hi-api/v1/properties?page=1&per_page=12&listing=residential&price_type=rent'
        yield scrapy.Request(url=urlbusinessrent, meta={'listingtype': 'business rent'})

    def parse(self, response, **kwargs):
        resjson = json.loads(response.text)
        resp = scrapy.Selector(text=resjson['page_button'])
        totalpages = int(resp.css('a')[-2].css('::Text').extract_first())
        i = 1
        while i <= totalpages:
            link = response.url.split('?page=1')[0] + f'?page={i}' + response.url.split('?page=1')[1]
            i += 1
            yield scrapy.Request(url=link, callback=self.parsedata, meta={'listingtype': response.meta['listingtype']})

    def parsedata(self, response):
        resjson = json.loads(response.text)
        for res in resjson['data']:
            item = dict()
            item['url'] = res['permalink']
            item['Domain'] = 'https://www.atrealty.com.au/'
            item['Listing Type'] = res['property_listing_type']
            item['Title'] = res['name']
            item['Street'] = res['property_address']
            item['Suburb'] = res['property_suburb']
            item['State'] = res['property_state']
            item['ZipCode'] = res['property_post_code']
            item['Property Type'] = res['property_type']
            item['Contact'] = res.css('::text').extract()[1]
            item['Property ID'] = res['id']
            item['TotalArea'] = res['property_base_size']
            item['Price'] = res['property_search_price']
            item['Bedrooms'] = res['property_no_of_bed']
            item['Bathrooms'] = res['property_no_of_bathrooms']
            item['ParkingSpaces'] = res['property_car_garages']
            item['Main Image'] = [{"url": res['property_images'][0]['url']}]
            imagelist = []
            for re in res['property_images']:
                imagelist.append(re['url'])
            item['Image'] = '\n'.join(imagelist)
            # item['Description'] = ' '.join(response.css('#property_description ::text').extract()).strip()
            processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(atrealty)
process.start()
