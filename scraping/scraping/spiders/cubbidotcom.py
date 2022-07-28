import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

processed = []

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class cubbidotcom(scrapy.Spider):
    name = 'cubbidotcom'

    def start_requests(self):
        url = f'https://www.cubbi.com.au/properties'
        res = requests.get(url=url)
        resSel = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resSel.css('.pager li')[-2].css('a span::text').extract_first())
        i = 1
        while i <= totalpages:
            url = f'https://www.cubbi.com.au/properties?page={i}'
            i += 1
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for resp in response.css('.explore-listings .widget-item')[:1]:
            try:
                price = resp.css('.price::text').extract_first()
                link = 'https://www.cubbi.com.au' + resp.css('.property-slider a::attr(href)').extract_first()
                yield scrapy.Request(url=link, callback=self.parse_data, meta={'price': price})
            except:
                pass

    def parse_data(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.cubbi.com.au/'
        if response.css('.label'):
            item['Listing Type'] = response.css('.label::text').extract_first()
        else:
            item['Listing Type'] = 'For Lease'
        item['Title'] = response.css('h1::text').extract_first()
        if 'Address available' not in item['Title']:
            if len(response.css('h1::text').extract_first().split()) == 3:
                try:
                    item['Street'] = ' '.join(response.css('h1::text').extract_first().split()[1:])
                except:
                    pass
        try:
            item['Suburb'] = response.css('h4::text').extract_first().split(',')[0]
        except:
            pass
        try:
            item['State'] = response.css('h4::text').extract_first().split(',')[1].split()[0]
        except:
            pass
        try:
            item['ZipCode'] = response.css('h4::text').extract_first().split(',')[1].split()[1]
        except:
            pass
        item['Price'] = response.meta['price']
        item['Contact'] = ''.join(response.css('.agent::text').extract()).strip()
        if len(response.url.split('-')) > 1:
            item['Property ID'] = response.url.split('-')[-1]
        else:
            item['Property ID'] = response.url.split('/')[-1]
        for res in response.css('.list.list-inline.icon-colour-primary li'):
            if res.css('.icon-badroom'):
                try:
                    item['Bedrooms'] = res.css('::text').extract()[1].strip()
                except:
                    pass
            if res.css('.icon-bathroom'):
                try:
                    item['Bathrooms'] = res.css('::text').extract()[1].strip()
                except:
                    pass
            if res.css('.icon-car'):
                try:
                    item['ParkingSpaces'] = res.css('::text').extract()[1].strip()
                except:
                    pass
        # item['TotalArea'] = response.css('.col-xs-12.marb20 .size::text').extract_first('')
        imagelist = []
        for i, res in enumerate(response.css('.pgwSlideshow li')):
            if i == 0:
                item['Main Image'] = [{"url": res.css('img::attr(src)').extract_first()}]
            else:
                imagelist.append(res.css('img::attr(src)').extract_first())
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ''.join(response.css('div.overview.content-section > p:nth-child(4)::text').extract()).strip()
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(cubbidotcom)
process.start()
