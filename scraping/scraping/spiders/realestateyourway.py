import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

rentlisturl = []
buylisturl = []
processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class realestateyourway(scrapy.Spider):
    name = 'realestateyourway'

    def start_requests(self):
        url = 'https://realestateyourway.com.au/properties/search?page=1&ipp=50&type=1'
        yield scrapy.Request(url=url, meta={'listingtype': 'buy'})
        url = 'https://realestateyourway.com.au/properties/search?page=1&ipp=50&type=2'
        yield scrapy.Request(url=url, meta={'listingtype': 'rent'})

    def parse(self, response, **kwargs):
        try:
            totalpages = int(response.css('.pagination li')[1:-1][-1].css('a::text').extract_first())
            i = 1
            while i <= totalpages:
                if 'buy' in response.meta['listingtype']:
                    url = response.url.split('?')[0] + f'?page={i}&ipp=50&type=1'
                if 'rent' in response.meta['listingtype']:
                    url = response.url.split('?')[0] + f'?page={i}&ipp=50&type=2'
                i += 1
                yield scrapy.Request(url=url, callback=self.parse_data, dont_filter=True, meta={'listingtype': response.meta['listingtype']})
        except:
            # if 'buy' in response.meta['listingtype']:
            #     url = response.url.split('?')[0] + f'?page={i}&ipp=50&type=1'
            # if 'rent' in response.meta['listingtype']:
            #     url = response.url.split('?')[0] + f'?page={i}&ipp=50&type=2'
            yield scrapy.Request(url=response.url, callback=self.parse_data, dont_filter=True, meta={'listingtype': response.meta['listingtype']})

    def parse_data(self, response):
        for res in response.css('#properties .col-sm-6'):
            url = 'https://realestateyourway.com.au' + res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_prop, meta={'listingtype': response.meta['listingtype']})

    def parse_prop(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://realestateyourway.com.au/'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('.property-title h1::text').extract_first('')
        i = 0
        tot = len(response.css('#quick-summary')[0].css('dl dt'))
        while i < tot:
            if 'Location' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['Street'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Price' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['Price'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Area' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['TotalArea'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Lot Size' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['TotalArea'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Bed' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['Bedrooms'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Bath' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['Bathrooms'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Garages' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['ParkingSpaces'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
            if 'Property Type' in response.css('#quick-summary')[0].css('dl dt')[i].css('::text').extract_first():
                item['Property Type'] = response.css('#quick-summary')[0].css('dl dd')[i].css('::text').extract_first()
        try:
            item['Suburb'] = item['Street'].split(',')[0]
        except:
            pass
        try:
            item['State'] = response.css('.section.content-section.main-heading-section h3::text').extract_first().split(',')[3]
        except:
            pass
        imagelist = []
        for i, img in enumerate(response.css('#property-gallery .property-slide')):
            if i == 0:
                item['Main Image'] = [{"url": 'https://realestateyourway.com.au' + img.css('a::attr(href)').extract_first('')}]
            else:
                imagelist.append('https://realestateyourway.com.au' + img.css('a::attr(href)').extract_first(''))
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ' '.join(response.css('#description')[-1].css(' ::text').extract())
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(realestateyourway)
process.start()
