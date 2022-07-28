import requests
import scrapy
from scrapy.crawler import CrawlerProcess

from AirtableApi import AirtableClient

cityname = []
statename = []
processed = []
basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


class noagentproperty(scrapy.Spider):
    name = 'noagentproperty'

    def start_requests(self):
        wikiresp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population')
        wikiresponce = scrapy.Selector(text=wikiresp.content.decode('utf-8'))
        for res in wikiresponce.css('table[class="wikitable sortable plainrowheaders"]')[0].css('tbody tr')[2:]:
            name = ''.join(res.css('td:nth-child(2) ::text').extract()).strip()
            state = ''.join(res.css('td:nth-child(3) ::text').extract()).strip()
            if '–' in name:
                n = name.split('–')
                cityname.append(n[0])
                cityname.append(n[0])

            else:
                cityname.append(name)

            if '/' in state:
                s = state.split('/')
                if s[0] == 'New South Wales':
                    s[0] = 'NSW'
                if s[0] == 'Queensland':
                    s[0] = 'QLD'
                if s[0] == 'South Australia':
                    s[0] = 'SA'
                if s[0] == 'Tasmania':
                    s[0] = 'TAS'
                if s[0] == 'Western Australia':
                    s[0] = 'WA'
                if s[0] == 'Australian Capital Territory':
                    s[0] = 'ACT'
                if s[0] == 'Jervis Bay Territory':
                    s[0] = 'ACT'
                if s[0] == 'Northern Territory':
                    s[0] = 'NT'
                if s[0] == 'Victoria':
                    s[0] = 'VIC'

                if s[1] == 'New South Wales':
                    s[1] = 'NSW'
                if s[1] == 'Queensland':
                    s[1] = 'QLD'
                if s[1] == 'South Australia':
                    s[1] = 'SA'
                if s[1] == 'Tasmania':
                    s[1] = 'TAS'
                if s[1] == 'Western Australia':
                    s[1] = 'WA'
                if s[1] == 'Australian Capital Territory':
                    s[1] = 'ACT'
                if s[1] == 'Jervis Bay Territory':
                    s[1] = 'ACT'
                if s[1] == 'Northern Territory':
                    s[1] = 'NT'
                if s[1] == 'Victoria':
                    s[1] = 'VIC'

                statename.append(s[0])
                statename.append(s[1])
            else:
                if state == 'New South Wales':
                    state = 'NSW'
                if state == 'Queensland':
                    state = 'QLD'
                if state == 'South Australia':
                    state = 'SA'
                if state == 'Tasmania':
                    state = 'TAS'
                if state == 'Western Australia':
                    state = 'WA'
                if state == 'Australian Capital Territory':
                    state = 'ACT'
                if state == 'Jervis Bay Territory':
                    state = 'ACT'
                if state == 'Northern Territory':
                    state = 'NT'
                if state == 'Victoria':
                    state = 'VIC'

                statename.append(state)
        for i, ur in enumerate(cityname):
            urlsale = f'https://www.noagentproperty.com.au/private-real-estate/for-sale/{statename[i]}/in-{ur}/listing-1/'
            yield scrapy.Request(url=urlsale, meta={'listingtype': 'buy'})
        for i, ur in enumerate(cityname):
            urlrent = f'https://www.noagentproperty.com.au/private-real-estate/rental/{statename[i]}/in-{ur}/listing-1/'
            yield scrapy.Request(url=urlrent, meta={'listingtype': 'rent'})

    def parse(self, response, **kwargs):
        try:
            lastpage = int((response.css('.navigation')[0].css('ul li')[-1].css('a::attr(href)').extract_first()).split('-')[-1])
            i = 1
            while i <= lastpage:
                url = response.url.split('/listing')[0] + f'/listing-{i}/'
                i += 1
                yield scrapy.Request(url=url, callback=self.parse_links, dont_filter=True, meta={'listingtype': response.meta['listingtype']})
        except:
            yield scrapy.Request(url=response.url, callback=self.parse_links, dont_filter=True, meta={'listingtype': response.meta['listingtype']})

    def parse_links(self, response):
        for res in response.css('ul.search-results.clearfix li.post-list'):
            link = res.css('a::attr(href)').extract_first()
            if link == None:
                continue
            yield scrapy.Request(url=link, callback=self.parse_data, meta={'listingtype': response.meta['listingtype']})

    def parse_data(self, response):
        item = dict()
        item['url'] = response.url
        item['Domain'] = 'https://www.noagentproperty.com.au/'
        item['Listing Type'] = response.meta['listingtype']
        item['Title'] = response.css('.search-result-brief.customPrint h1::text').extract_first('')
        try:
            item['State'] = response.css('.prop-address p::text').extract_first('').split()[-1]
        except:
            pass
        try:
            item['ZipCode'] = response.css('.prop-address p::text').extract_first('').split()[-2]
        except:
            pass
        try:
            if len(response.css('.prop-address p::text').extract_first().split()[:-2]) <= 2:
                item['Suburb'] = ' '.join(response.css('.prop-address p::text').extract_first('').split()[:-2])
        except:
            pass
        for res in response.css('.property-detail-inner li'):
            if 'Property ID' in res.css('span::text').extract_first():
                item['Property ID'] = res.css('em::text').extract_first()
            if 'Type' in res.css('span::text').extract_first():
                item['Property Type'] = res.css('em::text').extract_first()
            if 'Building Size' in res.css('span::text').extract_first():
                item['TotalArea'] = res.css('em::text').extract_first()
            if 'Bedrooms' in res.css('span::text').extract_first(''):
                item['Bedrooms'] = res.css('em::text').extract_first('')
            if 'Garages' in res.css('span::text').extract_first(''):
                item['ParkingSpaces'] = res.css('em::text').extract_first('')
            if 'Bathrooms' in res.css('span::text').extract_first(''):
                item['Bathrooms'] = res.css('em::text').extract_first('')
        try:
            item['Contact'] = response.css('.contact-owner-block ul li')[-1].css('span::text').extract_first('').strip()
        except:
            pass

        item['Price'] = response.css('.property-info h3::text').extract_first('')
        imagelist = []
        for i, img in enumerate(response.css('#sync2 .item.with-img')):
            if i == 0:
                item['Main Image'] = [{"url": img.css('img::attr(data-wpfc-original-src)').extract_first('')}]
            else:
                imagelist.append(img.css('img::attr(data-wpfc-original-src)').extract_first(''))
        item['Image'] = '\n'.join(imagelist)
        item['Description'] = ''.join(response.css('.property-content-outer p::text').extract())
        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(noagentproperty)
process.start()
