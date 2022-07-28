import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from AirtableApi import AirtableClient

rentlisturl = []
buylisturl = []
buylistpage = []
rentlistpage = []
processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)

class salehomeowner(scrapy.Spider):
    name = 'salehomeowner'

    def start_requests(self):
        wikiresp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population')
        wikiresponce = scrapy.Selector(text=wikiresp.content.decode('utf-8'))
        for res in wikiresponce.css('table[class="wikitable sortable plainrowheaders"]')[0].css('tbody tr')[2:]:
            name = ''.join(res.css('td:nth-child(2) ::text').extract()).strip()
            if '–' in name:
                n = name.split('–')
                buylisturl.append(f'https://www.salebyhomeowner.com.au/for-sale-by-owner-properties-2/?keyword={n[0]}')
                rentlisturl.append(f'https://www.salebyhomeowner.com.au/private-rentals-houses-for-rent-by-owner/?keyword={n[0]}')
                buylisturl.append(f'https://www.salebyhomeowner.com.au/for-sale-by-owner-properties-2/?keyword={n[1]}')
                rentlisturl.append(f'https://www.salebyhomeowner.com.au/private-rentals-houses-for-rent-by-owner/?keyword={n[1]}')
            else:
                buylisturl.append(f'https://www.salebyhomeowner.com.au/for-sale-by-owner-properties-2/?keyword={name}')
                rentlisturl.append(f'https://www.salebyhomeowner.com.au/private-rentals-houses-for-rent-by-owner/?keyword={name}')
        for url in buylisturl:
            yield scrapy.Request(url, callback=self.parse, meta={'listingtype': 'buy'})
        for url in rentlisturl:
            yield scrapy.Request(url, callback=self.parse, meta={'listingtype': 'rent'})
        # for url in buylistpage:
        #     yield scrapy.Request(url, callback=self.parse, meta={'listingtype': 'buy'})
        # for url in rentlistpage:
        #     yield scrapy.Request(url, callback=self.parse, meta={'listingtype': 'rent'})

    def parse(self, response, **kwargs):
        if not response.css('.no_properties_error'):
            totalresults = int(response.css('#sorter_pagination strong::text').extract_first())
            if totalresults < 10:
                yield scrapy.Request(response.url, callback=self.parse_pages, meta={'listingtype': response.meta['listingtype']}, dont_filter=True)
            else:
                page = totalresults / 10
                i = 1
                if page % 2 == 0:
                    while i <= page:
                        url = response.url + f'/{i}/'
                        i += 1
                        yield scrapy.Request(url, callback=self.parse_pages, meta={'listingtype': response.meta['listingtype']}, dont_filter=True)
                else:
                    while i <= (int(page) + 1):
                        url = response.url + f'/{i}/'
                        i += 1
                        yield scrapy.Request(url, callback=self.parse_pages, meta={'listingtype': response.meta['listingtype']}, dont_filter=True)

    def parse_pages(self, response):
        for resp in response.css('#thumbnail_format td'):
            try:
                link = resp.css('.landscape::attr(href)').extract_first()
                price = resp.css('.price::text').extract_first('')
                yield scrapy.Request(url=link, callback=self.parse_data, meta={'listingtype': response.meta['listingtype'], 'price': price})
            except:
                pass

    def parse_data(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.salebyhomeowner.com.au/'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('#details .property_address::text').extract_first('')
        try:
            item['Street'] = response.css('#details .property_address::text').extract_first().split(',')[0]
        except:
            pass
        try:
            item['Suburb'] = response.css('#details .property_address::text').extract_first().split(',')[1]
        except:
            pass
        try:
            item['State'] = response.css('#details .property_address::text').extract_first().split(',')[-1].split()[0]
        except:
            pass
        try:
            item['ZipCode'] = response.css('#details .property_address::text').extract_first().split(',')[-1].split()[1]
        except:
            pass
        item['Property Type'] = response.meta['listingtype']
        for res in response.css('#vendor_info_contact .vendor-information li'):
            if 'Contact Number:' in res.css('strong::text').extract_first(''):
                item['Contact'] = res.css('::text').extract_first('')
        for re in response.css('.side_land_size'):
            if 'Property ID ' in re.css('.field::text').extract_first():
                item['Property ID'] = re.css('.value span::text').extract_first('')
            if 'Building Size' in re.css('.field::text').extract_first():
                item['TotalArea'] = re.css('.value span::text').extract_first('')
        item['Price'] = response.meta['price']
        item['Bedrooms'] = response.css('.rooms .bedrooms::text').extract_first('')
        item['Bathrooms'] = response.css('.rooms .bathrooms::text').extract_first('')
        item['ParkingSpaces'] = response.css('.rooms .carspaces::text').extract_first('')
        imagelist = []
        for i, img in enumerate(response.css('#thumbnails ul li')):
            if i == 0:
                item['Main Image'] = [{"url": img.css('a::attr(href)').extract_first('')}]
            else:
                imagelist.append(img.css('a::attr(href)').extract_first())
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ' '.join(response.css('#property_description ::text').extract()).strip()
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(salehomeowner)
process.start()
