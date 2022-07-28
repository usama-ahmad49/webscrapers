import csv

import scrapy
from scrapy.crawler import CrawlerProcess

header = ["name", "city", "map_link", "address", "website", "added", "updated", "checked", "email"]

file = open('data.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()


class RunningIntheusa(scrapy.Spider):
    name = 'runningintheusa'
    start_urls = ['https://www.runningintheusa.com/club/find-by-state/']

    def parse(self, response):
        for state in response.css('#text-abb text ::Text').extract()[:1]:
            url = 'https://www.runningintheusa.com/club/list/{}'.format(state.lower())
            url = 'https://www.runningintheusa.com/club/list/{}'.format('wa'.lower())
            yield scrapy.Request(url, callback=self.parse_pages, meta={'state': state.lower()})

    def parse_pages(self, response):
        total_records = int(
            [v.strip() for v in response.css('.pagination.pagination-sm ::text').extract() if v.strip() and 'of' in v][
                0].split('of')[1].strip())

        for url in [v for v in response.css('.btn-group-vertical a::attr(href)').extract() if 'details/' in v]:
            url = 'https://www.runningintheusa.com{}'.format(url)
            yield scrapy.Request(url, callback=self.parse_details)
        if response.meta.get('state'):
            for i in range(1, int(total_records / 20) + 1):
                url = 'https://www.runningintheusa.com/club/list/{}/page-{}'.format(response.meta['state'], i+1)
                yield scrapy.Request(url, callback=self.parse_pages)

    def parse_details(self, response):
        item = dict()
        for row in response.css('.panel.panel-primary .list-group .list-group-item'):
            if 'Name' in ''.join(row.css('.col-sm-3.text-primary ::text').extract()):
                item['name'] = ' '.join(row.css('.col-sm-9 ::text').extract()).strip()
            if 'Primary' in ''.join(row.css('.col-sm-3.text-primary ::text').extract()):
                item['website'] = 'https://www.runningintheusa.com{}'.format(row.css('a ::attr(href)').extract_first(''))
            if 'City' in ''.join(row.css('.col-sm-3.text-primary ::text').extract()):
                item['city'] = ' '.join(row.css('.col-sm-3:nth-child(2) ::text').extract()).strip()
                item['map_link'] = row.css('.col-sm-3:nth-child(3) a::attr(href)').extract_first().strip()
                item['address'] = ' '.join(row.css('.col-sm-3:nth-child(4) ::text').extract()).strip()

        try:
            selected_div = [v for v in response.css('.panel.panel-info') if
             'Listing Status' in ''.join(v.css('.panel-heading ::text').extract())][0]
            for row in selected_div.css('.list-group-item'):
                if 'Added' in ''.join(row.css('.col-sm-6.text-primary ::Text').extract()):
                    item['added'] = ''.join(row.css('.col-sm-3 ::Text').extract()).strip()
                if 'Updated' in ''.join(row.css('.col-sm-6.text-primary ::Text').extract()):
                    item['updated'] = ''.join(row.css('.col-sm-3 ::Text').extract()).strip()
                if 'checked' in ''.join(row.css('.col-sm-6.text-primary ::Text').extract()):
                    item['checked'] = ''.join(row.css('.col-sm-3 ::Text').extract()).strip()
        except:
            pass
        yield scrapy.Request(item['website'], callback=self.parse_email, meta={'item': item})

    def parse_email(self, response):
        item = response.meta['item']
        text = ' '.join(response.css('::text').extract())
        emails = [v for v in text.replace('@ ', '@').split(' ') if '@' in v and '.' in v]
        emails = list(set(emails))
        item['email'] = emails[0] if emails else ''
        item['email'] = item['email'].split(':')[1] if ':' in item['email'] else item['email']
        item['email'] = item['email'][:item['email'].find('.com') + 4] if '.com' in item['email'] else ''
        item['email'] = item['email'].replace('"', '')
        writer.writerow(item)
        file.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(RunningIntheusa)
process.start()
