import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)
processed = []


class minustheagentDomain(scrapy.Spider):
    name = 'minustheagentDomain'

    def start_requests(self):
        url = 'https://www.domain.com.au/real-estate-agencies/minustheagent-26625/'
        req = requests.get(url=url)
        reqSel = scrapy.Selector(text=req.content.decode('utf-8'))
        for listingtype in reqSel.css('#listings .css-miyrqm button'):
            url = f"https://www.domain.com.au/real-estate-agencies/minustheagent-26625/?tab={listingtype.css('::text').extract_first().replace(' ', '-').lower()}"
            reqlisting = requests.get(url=url)
            reqSellisting = scrapy.Selector(text=reqlisting.content.decode('utf-8'))
            totalpages = int(reqSellisting.css('#fe-pa-agency-profile-paginator .css-1ytqxcs a')[-1].css('::text').extract_first())
            i = 1
            while i <= totalpages:
                link = url + f"&tab-page={i}"
                i += 1
                yield scrapy.Request(url=link, meta={'listingtype': listingtype.css('::text').extract_first()})

    def parse(self, response, **kwargs):
        for resp in response.css('#listings .css-xvdn3b'):
            url = "https:" + resp.css('.css-1abqvvq::attr(href)').extract_first()
            try:
                street = resp.css('span[data-testid="address-line1"]::text').extract_first()
            except:
                street = ''
            try:
                suburb = resp.css('span[itemprop="addressLocality"]::text').extract_first()
            except:
                suburb = ''
            try:
                state = resp.css('span[itemprop="addressRegion"]::text').extract_first()
            except:
                state = ''
            try:
                postcode = resp.css('span[itemprop="postalCode"]::text').extract_first()
            except:
                postcode = ''
            try:
                price = resp.css('p[data-testid="listing-card-price"]::text').extract_first()
            except:
                price = ''
            yield scrapy.Request(url=url, callback=self.parse_data, meta={'listingtype': response.meta['listingtype'], 'street': street, 'suburb': suburb, 'state': state, 'postcode': postcode, 'price': price})

    def parse_data(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.minustheagent.com.au/'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('h1::text').extract_first()
        try:
            item['Street'] = response.meta['street']
        except:
            pass
        try:
            item['Suburb'] = response.meta['suburb']
        except:
            pass
        try:
            item['State'] = response.meta['state']
        except:
            pass
        try:
            item['ZipCode'] = response.meta['postcode']
        except:
            pass
        item['Property Type'] = response.css('div[data-testid="listing-summary-property-type"] .css-in3yi3::text').extract_first()
        item['Contact'] = response.css('.css-1e450r1::attr(href)').extract_first().split(':')[1]
        try:
            item['Property ID'] = response.url.split('-')[-1]
        except:
            pass
        for res in response.css('.css-1ewgpst div[data-testid="property-features-wrapper"] .css-1ie6g1l'):
            if 'M4.00002' in res.css('svg path:nth-child(1)::attr(d)').extract_first():
                item['Bedrooms'] = res.css('.css-1rzse3v::text').extract_first().strip()
            if 'M6 19v2M18 19v2' in res.css('svg path:nth-child(1)::attr(d)').extract_first():
                item['Bathrooms'] = res.css('.css-1rzse3v::text').extract_first().strip()
            if 'M21 10h-2M5 10H3' in res.css('svg path:nth-child(1)::attr(d)').extract_first():
                item['ParkingSpaces'] = res.css('.css-1rzse3v::text').extract_first().strip()
            if 'M3.5 4v13' in res.css('svg path:nth-child(1)::attr(d)').extract_first():
                item['TotalArea'] = res.css('.css-1rzse3v::text').extract_first().strip()

        try:
            item['Price'] = response.meta['price']
        except:
            pass

        item['Main Image'] = [{"url": response.css('div[data-testid="listing-details__gallery"] .css-1azjcl img::attr(src)').extract_first()}]
        imagelist = []
        for img in response.css('div[data-testid="listing-details__gallery"] .css-ml426i .css-xsxs71'):
            imagelist.append(img.css('img::attr(src)').extract_first())
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ' '.join(response.css('div[name="listing-details__description"] .noscript-expander-content.css-1mnayj9 p ::text').extract()).strip()
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(minustheagentDomain)
process.start()
