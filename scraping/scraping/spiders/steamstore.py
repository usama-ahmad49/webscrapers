import csv
import json
import re

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

resp = requests.get(
    'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1')
total_count = json.loads(resp.text)['total_count']

headers_csv = ['email', 'game_name', 'release_date', 'pre-release', 'is_NSFW']
csvfile = open('steamStore.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
writer.writeheader()


def get_email(page_text):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_text)
    emails = [v for v in set(emails)]
    return emails


class steamStore(scrapy.Spider):
    name = 'steamStore'

    def __init__(self, NSFW=None, **kwargs):
        super().__init__(**kwargs)
        self.NSFW = NSFW

    def start_requests(self):
        start_count = 0
        while start_count < total_count:
            if self.NSFW == True:
                url = f'https://store.steampowered.com/search/results/?query&start={start_count}&count=50&ignore_preferences=1&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1'
            else:
                url = f'https://store.steampowered.com/search/results/?query&start={start_count}&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1'
            start_count = start_count + 50
            yield scrapy.Request(url=url)

        # url = 'https://store.steampowered.com/app/1362120/PIGROMANCE/'
        # yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        # links = response.css('div#search_result_container a.search_result_row.ds_collapse_flag::attr(href)').extract()

        js = json.loads(response.text)
        rp = scrapy.Selector(text=js['results_html'])
        for url in rp.css('a'):
            link = url.css('::attr(href)').get()
            game_name = url.css('span.title::text').get()
            release_date = url.css('div.col.search_released.responsive_secondrow::text').get()
            yield scrapy.Request(url=link, callback=self.next_parse, meta={'name': game_name, 'date': release_date})

    def next_parse(self, response):
        game_name = response.meta['name']
        release_date = response.meta['date']
        if len([v for v in response.css('#glanceCtnResponsiveRight .app_tag::text').extract() if 'NSFW' in v]) < 1:
            NSFWFlag = False
        else:
            NSFWFlag = True
        # if NSFWFlag:
        #     return
        flag = False
        for lang in response.css('#languageTable td ::text').extract():
            if 'English' in lang:
                flag = True
            if 'Spanish' in lang:
                flag = False
        if not flag:
            return
        page_text = " ".join([v for v in response.css(" ::text").extract()])
        try:
            email = ','.join(get_email(page_text))
        except:
            email = None
        developers = [v for v in response.css('.dev_row') if 'Developer:' in v.css('.subtitle.column::text').extract()][0].css('.summary.column a::text').extract_first()
        publishers = [v for v in response.css('.dev_row') if 'Publisher:' in v.css('.subtitle.column::text').extract()][0].css('.summary.column a::text').extract_first()
        externalLinks = [v.split('?url=')[-1] for v in
                         response.css('#appDetailsUnderlinedLinks .linkbar ::attr(href)').extract() if
                         'steamcommunity.com' in v and '?url=' in v]

        if email is None or email == "":
            for extlnk in externalLinks:
                yield scrapy.Request(url=extlnk, callback=self.next_page_resp,
                                     meta={'name': game_name, 'date': release_date, 'developer':developers,'publisher':publishers,'is_NSFW':NSFWFlag})
        else:
            item = dict()
            item['game_name'] = response.meta['name']
            if 'Coming soon' in response.meta['date']:
                item['pre-release'] = 'Yes'
            else:
                item['release_date'] = response.meta['date']
            item['email'] = email
            item['developers'] = developers
            item['publishers'] = publishers
            item['is_NSFW'] = NSFWFlag

            writer.writerow(item)
            csvfile.flush()

    def next_page_resp(self, response):
        item = dict()
        page_text = " ".join([v for v in response.css(" ::text").extract()])
        try:
            email = ','.join(get_email(page_text))
        except:
            pass

        item['game_name'] = response.meta['name']
        if 'Coming soon' in response.meta['date']:
            item['pre-release'] = 'Yes'
        else:
            item['release_date'] = response.meta['date']
        item['developers'] = response.meta['developer']
        item['publishers'] = response.meta['publisher']
        item['is_NSFW'] = response.meta['NSFWFlag']
        if email is not None:
            if email != "":
                item['email'] = email

        writer.writerow(item)
        csvfile.flush()


def startscraper(NSFWFLAG):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(steamStore, NSFW=NSFWFLAG)
    process.start()

if __name__ == '__main__':
    startscraper(NSFWFLAG = False)