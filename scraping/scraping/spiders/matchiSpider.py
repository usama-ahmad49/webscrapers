try:
    import pkg_resources.py2_warn
except ImportError:
    pass

from scrapy.crawler import CrawlerProcess
import scrapy
import csv
from datetime import datetime
# '2020-10-30', '2020-11-1', '2020-11-2',
datelist = ['2020-10-30', '2020-11-1', '2020-11-2','2020-11-03']

headers = ["facility_id", "facility_name", "city", "slot_id", "date", "time", "court", "playing_time", "sport", "court_type", "outdoor", "booking_url"]
file = open('matchiSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=headers)
writer.writeheader()


class matchiSpider(scrapy.Spider):
    name = 'matchispider'
    title = 'MatchiSpider'
    lat = ''
    lng = ''
    offset = 0
    outdoors = ''
    sport = 5
    q = 'stockholm'#'göteborg'
    hascamera = ''

    def start_requests(self):

        for date in datelist:
            url = 'https://www.matchi.se/book/findFacilities/index?lat={}&lng={}&offset=0&outdoors={}&sport={}&date={}&q={}&hasCamera={}&max=10'.format(self.lat, self.lng, self.outdoors, self.sport, date, self.q, self.hascamera)
            yield scrapy.Request(url=url, callback=self.parse, meta={'date': date})

    def parse(self, response):

        try:
            total_results = int(response.xpath('/html/body/div[11]/div/nav/div/span[2]/text()').extract_first().split(' ')[0])
        except:
            total_results = 0
        if total_results == 0:
            pages = 1
        elif total_results % 10 == 0:
            pages = total_results / 10
        elif total_results % 10 < 5:
            pages = (round(total_results / 10)) + 1
        else:
            pages = round(total_results / 10)
        i = 1
        offset=0
        while i <= pages:
            url = 'https://www.matchi.se/book/findFacilities/index?lat={}&lng={}&offset={}&outdoors={}&sport={}&date={}&q={}&hasCamera={}&max=10'.format(self.lat, self.lng, offset, self.outdoors, self.sport, response.meta['date'], self.q, self.hascamera)
            yield scrapy.Request(url=url, callback=self.parse_data,dont_filter=True)
            i = i + 1
            offset = offset + 10

    def parse_data(self, response):
        for resp in response.xpath('/html/body/div')[:-1]:
            item = dict()
            id = resp.xpath('div/div[1]/div[1]/div/div[2]/div/a/@href').extract_first()
            item['facility_id'] = ((id.split('/')[3]).split('=')[1]).split('&')[0]
            item['facility_name'] = resp.xpath('div/div[1]/div[1]/div/div[2]/h3/a/text()').extract_first().strip()
            item['city'] = resp.xpath('div/div[1]/div[1]/div/div[2]/p/text()').extract_first().strip()
            for avilibility in resp.xpath('div/div[1]/div[2]/div[1]/div'):
                item['date'] = datetime.strptime((avilibility.xpath('ul/li[1]/h6/strong[1]/text()').extract_first().strip()).split(', ')[1].replace(' ', '-'), '%d-%b-%Y').strftime('%Y-%m-%d')
                item['time'] = avilibility.xpath('ul/li[1]/h6/strong[2]/text()').extract_first().strip() + ':' + avilibility.xpath('ul/li[1]/h6/strong[2]/sup/text()').extract_first().strip()
                item['slot_id'] = datetime.strptime((item['date'] + ' ' + item['time']), '%Y-%m-%d %H:%M').strftime('%y%m%d%H%M')
                for individualcourts in avilibility.xpath('ul/li')[1:]:
                    item['court'] = individualcourts.xpath('table/tr/td[1]/text()').extract_first().strip()
                    item['playing_time'] = individualcourts.xpath('table/tr/td[2]/text()').extract_first().strip().replace('min', '')
                    item['sport'] = individualcourts.xpath('table/tr/td[3]/div[1]/text()').extract_first().strip()
                    item['court_type'] = individualcourts.xpath('table/tr/td[3]/div[2]/small/text()').extract_first().strip()
                    try:
                        item['outdoor'] = individualcourts.xpath('table/tr/td[3]/div[3]/small/text()').extract_first().replace('(','').replace(')','')
                    except:
                        item['outdoor'] = ' - '
                    item['booking_url'] = 'https://www.matchi.se' + individualcourts.xpath('table/tr/td[4]/a/@href').extract_first()
                    writer.writerow(item)
                    file.flush()
        # yield item


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(matchiSpider)
process.start()
