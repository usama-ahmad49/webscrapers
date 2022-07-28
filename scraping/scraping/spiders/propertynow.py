import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

rentlisturl = []
buylisturl = []

saleurllist = []
renturllist = []
landurllist = []
comrenturllist = []
businessurllist = []
ruralurllist = []
processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class propertynow(scrapy.Spider):
    name = 'realestateyourway'

    def start_requests(self):
        gotsale = True
        i = 1
        while gotsale:
            urlsale = f'https://app.propertynow.com.au/search-properties/buy/list-{i}'
            i += 1
            resale = requests.get(url=urlsale)
            resaleSel = scrapy.Selector(text=resale.content.decode('utf-8'))
            if 'No result' in resaleSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotsale = False
            for link in resaleSel.css('#search-results .listing-link'):
                saleurllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())
        gotrent = True
        i = 1
        while gotrent:
            urlrent = f'https://app.propertynow.com.au/search-properties/rent/list-{i}'
            i += 1
            rerent = requests.get(url=urlrent)
            rerentSel = scrapy.Selector(text=rerent.content.decode('utf-8'))
            if 'No result' in rerentSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotrent = False
            for link in rerentSel.css('#search-results .listing-link'):
                renturllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())
        gotlandsale = True
        i = 1
        while gotlandsale:
            urlcomertailsale = f'https://app.propertynow.com.au/search-properties/land/list-{i}'
            i += 1
            recomertailsale = requests.get(url=urlcomertailsale)
            recomertailsaleSel = scrapy.Selector(text=recomertailsale.content.decode('utf-8'))
            if 'No result' in recomertailsaleSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotlandsale = False
            for link in recomertailsaleSel.css('#search-results .listing-link'):
                landurllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())
        gotcomsale = True
        i = 1
        while gotcomsale:
            urlcomsale = f'https://app.propertynow.com.au/search-properties/commercial/list-{i}'
            i += 1
            recommercial = requests.get(url=urlcomsale)
            recommercialSel = scrapy.Selector(text=recommercial.content.decode('utf-8'))
            if 'No result' in recommercialSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotcomsale = False
            for link in recommercialSel.css('#search-results .listing-link'):
                comrenturllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())
        gotbusiness = True
        i = 1
        while gotbusiness:
            urlbus = f'https://app.propertynow.com.au/search-properties/business/list-{i}'
            i += 1
            recommercial = requests.get(url=urlbus)
            recommercialSel = scrapy.Selector(text=recommercial.content.decode('utf-8'))
            if 'No result' in recommercialSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotbusiness = False
            for link in recommercialSel.css('#search-results .listing-link'):
                businessurllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())
        gotrural = True
        i = 1
        while gotrural:
            urlrural = f'https://app.propertynow.com.au/search-properties/rural/list-{i}'
            i += 1
            recommercial = requests.get(url=urlrural)
            recommercialSel = scrapy.Selector(text=recommercial.content.decode('utf-8'))
            if 'No result' in recommercialSel.css('#search-results > div > div:nth-child(2) > strong::text').extract_first(''):
                gotrural = False
            for link in recommercialSel.css('#search-results .listing-link'):
                ruralurllist.append('https://app.propertynow.com.au' + link.css('::attr(href)').extract_first())

        for link in saleurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'buy'})
        for link in renturllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'rent'})
        for link in landurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'land buy'})
        for link in comrenturllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'commercial buy'})
        for link in businessurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'business buy'})
        for link in ruralurllist:
            yield scrapy.Request(url=link, meta={'listingtype': 'rural buy'})

    def parse(self, response, **kwargs):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'propertynow.com.au'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('h1.text-center.mb-4 ::text').extract_first('').strip()
        try:
            item['Street'] = response.css('h1.text-center.mb-4 ::text').extract_first('').strip().split(',')[0]
        except:
            pass
        try:
            item['Suburb'] = response.css('h1.text-center.mb-4 ::text').extract_first('').strip().split(',')[1]
        except:
            pass
        try:
            item['State'] = response.css('h1.text-center.mb-4 ::text').extract_first('').strip().split(',')[2]
        except:
            pass
        try:
            item['ZipCode'] = response.css('h1.text-center.mb-4 ::text').extract_first('').strip().split(',')[3]
        except:
            pass
        try:
            item['Price'] = response.css('.col-md-12.acenter.marb20 h2::text').extract_first().strip()
        except:
            pass
        item['Contact'] = response.css('.keyinfo.phone::text').extract_first('')
        try:
            item['Property ID'] = response.url.split('/')[-1]
        except:
            pass
        item['TotalArea'] = response.css('.col-xs-12.marb20 .size::text').extract_first('')
        item['Bedrooms'] = response.css('.col-xs-12.marb20 .bed::text').extract_first('')
        item['Bathrooms'] = response.css('.col-xs-12.marb20 .bath::text').extract_first('')
        item['ParkingSpaces'] = response.css('.col-xs-12.marb20 .garage::text').extract_first('')
        imagelist = []
        for i, res in enumerate(response.css('#ninja-slider ul li')):
            if i == 0:
                item['Main Image'] = [{"url": res.css('a::attr(href)').extract_first('')}]
            else:
                imagelist.append(res.css('a::attr(href)').extract_first(''))
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ''.join(response.css('.description ::text').extract()).strip()
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(propertynow)
process.start()
