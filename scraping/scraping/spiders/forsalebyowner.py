import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

saleurllist = []
renturllist = []
comsaleurllist = []
comrenturllist = []
processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class forsaleowner(scrapy.Spider):
    name = 'forsaleowner'

    def start_requests(self):
        gotsale = True
        i = 25
        while gotsale:
            urlsale = f'https://www.forsalebyowner.com.au/search-residential-sales/?cpage={i}'
            i += 1
            resale = requests.get(url=urlsale)
            resaleSel = scrapy.Selector(text=resale.content.decode('utf-8'))
            if 'No Properties in' in resaleSel.css('#result > h2::text').extract_first(''):
                gotsale = False
            for link in resaleSel.css('#result .search-results.card.clearfix'):
                saleurllist.append(link.css('.ppt-image.col-md-6 a::attr(href)').extract_first())
        gotrent = True
        i = 1
        while gotrent:
            urlrent = f'https://www.forsalebyowner.com.au/search-residential-rentals/?cpage={i}'
            i += 1
            rerent = requests.get(url=urlrent)
            rerentSel = scrapy.Selector(text=rerent.content.decode('utf-8'))
            if 'No Properties in' in rerentSel.css('#result > h2::text').extract_first(''):
                gotrent = False
            for link in rerentSel.css('#result .search-results.card.clearfix'):
                renturllist.append(link.css('.ppt-image.col-md-6 a::attr(href)').extract_first())
        gotcomsale = True
        i = 1
        while gotcomsale:
            urlcomertailsale = f'https://www.forsalebyowner.com.au/search-commercial-sales/?cpage={i}'
            i += 1
            recomertailsale = requests.get(url=urlcomertailsale)
            recomertailsaleSel = scrapy.Selector(text=recomertailsale.content.decode('utf-8'))
            if 'No Properties in' in recomertailsaleSel.css('#result > h2::text').extract_first(''):
                gotcomsale = False
            for link in recomertailsaleSel.css('#result .search-results.card.clearfix'):
                comsaleurllist.append(link.css('.ppt-image.col-md-6 a::attr(href)').extract_first())
        gotcomrent = True
        i = 1
        while gotcomrent:
            urlcomertailrent = f'https://www.forsalebyowner.com.au/search-commercial-rentals?cpage={i}'
            i += 1
            recomertailrent = requests.get(url=urlcomertailrent)
            recomertailrentSel = scrapy.Selector(text=recomertailrent.content.decode('utf-8'))
            if 'No Properties in' in recomertailrentSel.css('#result > h2::text').extract_first(''):
                gotcomrent = False
            for link in recomertailrentSel.css('#result .search-results.card.clearfix'):
                comrenturllist.append(link.css('.ppt-image.col-md-6 a::attr(href)').extract_first())

        for link in saleurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'buy'})
        for link in renturllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'rent'})
        for link in comsaleurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'commercial buy'})
        for link in comrenturllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'commercial rent'})

    def parse(self, response, **kwargs):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.forsalebyowner.com.au/'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('.heading-description h3::text').extract_first('')
        if len(response.css('.property-address::text').extract_first('').split(',')) < 3:
            try:
                item['Suburb'] = response.css('.property-address::text').extract_first('').split(',')[0]
            except:
                pass
            try:
                item['State'] = response.css('.property-address::text').extract_first('').split(',')[1].split()[0]
            except:
                pass
            try:
                item['ZipCode'] = response.css('.property-address::text').extract_first('').split(',')[1].split()[1]
            except:
                pass
        else:
            try:
                item['Street'] = response.css('.property-address::text').extract_first('').split(',')[0]
            except:
                pass
            try:
                item['Suburb'] = response.css('.property-address::text').extract_first('').split(',')[1]
            except:
                pass
            try:
                item['State'] = response.css('.property-address::text').extract_first('').split(',')[2].split()[0]
            except:
                pass
            try:
                item['ZipCode'] = response.css('.property-address::text').extract_first('').split(',')[2].split()[1]
            except:
                pass
        try:
            item['Price'] = response.css('.property-price ::text').extract_first('').strip().split(':')[-1]
        except:
            item['Price'] = response.css('.property-price ::text').extract_first('').strip()
        item['Contact'] = response.css('#property-code-container strong::text').extract_first('')
        item['Property ID'] = response.css('#property-code-container .property-code-2::text').extract_first('')
        if 'Floor Area' in response.css('.property-features::text').extract_first('').strip():
            item['TotalArea'] = response.css('.property-features::text').extract_first('').strip().split(': ')[-1]
        item['Bedrooms'] = response.css('.mini-details .bedrooms::text').extract_first('')
        item['Bathrooms'] = response.css('.mini-details .bathrooms::text').extract_first('')
        item['ParkingSpaces'] = response.css('.mini-details .carspaces::text').extract_first('')
        imagelist = []
        item['Main Image'] = [{"url": response.css('#firstimage::attr(href)').extract_first('')}]
        for res in response.css('.mosaic-img-secondary .secondary-images'):
            imagelist.append(res.css('a::attr(href)').extract_first(''))
        item['Image'] = '\n'.join(imagelist)
        try:
            item['Description'] = ''.join(response.css('.property_description ::text').extract()).strip()
        except:
            pass
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(forsaleowner)
process.start()
