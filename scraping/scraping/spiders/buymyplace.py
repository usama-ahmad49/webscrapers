import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

rentlisturl = []
buylisturl = []
buypropurllist = []
rentpropurllist = []
processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class buymyplace(scrapy.Spider):
    name = 'propertiesdat'

    def start_requests(self):
        wikiresp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population')
        wikiresponce = scrapy.Selector(text=wikiresp.content.decode('utf-8'))
        for res in wikiresponce.css('table[class="wikitable sortable plainrowheaders"]')[0].css('tbody tr')[2:]:
            name = ''.join(res.css('td:nth-child(2) ::text').extract()).strip()
            if '–' in name:
                n = name.split('–')
                buylisturl.append(f'https://buymyplace.com.au/buy-property/listings/{n[0]}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
                rentlisturl.append(f'https://buymyplace.com.au/lease-rent-your-property/listings/{n[0]}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
                buylisturl.append(f'https://buymyplace.com.au/buy-property/listings/{n[1]}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
                rentlisturl.append(f'https://buymyplace.com.au/lease-rent-your-property/listings/{n[1]}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
            else:
                buylisturl.append(f'https://buymyplace.com.au/buy-property/listings/{name}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
                rentlisturl.append(f'https://buymyplace.com.au/lease-rent-your-property/listings/{name}/anyPropertyTypes/anyMinPrice/anyMaxPrice/anyMinBeds/anyMinBaths/surround/500/0')
        for url in buylisturl[:2]:
            yield scrapy.Request(url=url, meta={'listingtype': 'buy'})
        for url in rentlisturl[:2]:
            yield scrapy.Request(url=url, meta={'listingtype': 'rent'})

    def parse(self, response, **kwargs):
        listtype = response.meta['listingtype']
        for resp in response.css('.bmp-tiles a.property-item'):
            indpropurl = 'https://buymyplace.com.au' + resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=indpropurl, callback=self.parsedata, meta={'listingtype': listtype})

    def parsedata(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://buymyplace.com.au'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('.section.content-section.main-heading-section h3::text').extract_first('')
        try:
            item['Street'] = response.css('.section.content-section.main-heading-section h3::text').extract_first().split(',')[1]
        except:
            pass
        try:
            item['Suburb'] = response.css('.section.content-section.main-heading-section h3::text').extract_first().split(',')[2]
        except:
            pass
        try:
            item['State'] = response.css('.section.content-section.main-heading-section h3::text').extract_first().split(',')[3]
        except:
            pass
        item['Property Type'] = response.css('.row.propertyType::text').extract_first('').strip()
        item['Contact'] = response.css('.row.contact a::text').extract_first('').strip()
        item['Property ID'] = response.css('.row.property-id::text').extract_first('').strip()
        item['Price'] = response.css('.row.subheading h4::text').extract_first('').strip()
        item['Bedrooms'] = response.css('.bed ::text').extract_first('').strip()
        item['Bathrooms'] = response.css('.bath ::text').extract_first('').strip()
        item['ParkingSpaces'] = response.css('.bath ::text').extract_first('').strip()
        item['TotalArea'] = response.css('.area ::text').extract_first('').strip()
        imagelist = []
        for i, img in enumerate(response.css('.carousel-inner .carousel-item')):
            if i == 0:
                item['Main Image'] = [{"url": img.css(' ::attr(src)').extract_first('')}]
            else:
                imagelist.append(img.css(' ::attr(src)').extract_first(''))
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ' '.join(response.css('.row.description::text').extract())
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(buymyplace)
process.start()
