import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

urllist = []
processed = []
basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class minustheagent(scrapy.Spider):
    name = 'minustheagent'

    def start_requests(self):
        url = 'https://www.minustheagent.com.au/search-properties/'
        res = requests.get(url)
        ressel = scrapy.Selector(text=res.content.decode('utf-8'))
        totalresults = int(ressel.css('#sorter_pagination strong::text').extract_first())
        pages = totalresults / 20
        if not pages.is_integer():
            pages = int(pages) + 1
        else:
            pass
        i = 1
        while i <= pages:
            url = f'https://www.minustheagent.com.au/search-properties/{i}/'
            i += 1
            res = requests.get(url)
            ressel = scrapy.Selector(text=res.content.decode('utf-8'))
            for res in ressel.css('#list-mode .listing'):
                urllist.append(res.css('.image a::attr(href)').extract_first())
        for link in urllist:
            yield scrapy.Request(url=link, dont_filter=True)

    def parse(self, response, **kwargs):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.minustheagent.com.au/'
        # item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('h2.title::text').extract_first().strip()
        try:
            item['Street'] = response.css('h1.title::text').extract_first().strip().split(',')[0]
        except:
            pass
        try:
            item['Suburb'] = response.css('h1.title::text').extract_first().strip().split(',')[-1].split()[0]
        except:
            pass
        try:
            item['State'] = response.css('h1.title::text').extract_first().strip().split(',')[-1].split()[1]
        except:
            pass
        try:
            item['ZipCode'] = response.css('#details .property_address::text').extract_first().split(',')[-1].split()[1]
        except:
            pass
        item['Property Type'] = response.css('.property_type .value::text').extract_first()
        item['Contact'] = response.css('.agent_phone.ph span::text').extract_first().strip()
        try:
            item['Property ID'] = response.url.replace('/', '').split('-')[-1]
        except:
            pass
        # item['TotalArea'] = re.css('.value span::text').extract_first()
        try:
            item['Price'] = response.css('h3.title ::text').extract_first().strip().split(":")[-1].split()[0]
        except:
            pass
        item['Bedrooms'] = response.css('.bedrooms .num::text').extract_first()
        item['Bathrooms'] = response.css('.bathrooms .num::text').extract_first()
        # item['ParkingSpaces'] = response.css('.rooms .carspaces::text').extract_first()
        imagelist = []
        for i, img in enumerate(response.css('#realty_widget_media script[type="text/javascript"]').extract()[1].split('thumbimages[')[1:-4]):
            if i == 0:
                item['Main Image'] = [{"url": img.split('thumbimages[')[0].split('src=')[-1].split('&')[0]}]
            else:
                imagelist.append(img.split('thumbimages[')[0].split('src=')[-1].split('&')[0])
        item['Image'] = '\n'.join(imagelist)
        try:
            item['Description'] = ''.join(response.css('.property-description.s-lrpad ::text').extract()).strip()
        except:
            pass
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(minustheagent)
process.start()
