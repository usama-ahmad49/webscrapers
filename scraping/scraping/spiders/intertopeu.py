import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

skipsports = ['Curling', 'Cycling', 'Darts', 'Entertainment', 'Futsal', 'Handball', 'Horses Futures', 'Motor Sports', 'Numbers Game', 'Other Sports', 'Politics',
              'Prop Builder', 'Snooker', 'Esports', 'Winter Olympics']
fileout = open('intertopeu.json', 'w')


class intertopeu(scrapy.Spider):
    name = 'intertopeu'
    items = []

    def start_requests(self):
        url = 'https://sports.intertops.eu/en/'
        firstPageResponse = requests.get(url=url)
        firstPageResponse = scrapy.Selector(text=firstPageResponse.content.decode('utf-8'))
        for res in firstPageResponse.css('#sports-nav ul.menu.br'):
            sports = res.css('li.scroller ul li.smh a .title.cl-ttl::text').extract_first()
            if sports in skipsports:
                continue
            for resp in res.css('li.scroller ul li.lg'):
                url = 'https://sports.intertops.eu' + resp.css('a::attr(href)').extract_first()
                league = resp.css('a::text').extract_first()
                yield scrapy.Request(url=url, meta={'sports': sports, 'league': league})

    def parse(self, response, **kwargs):
        items = []
        for res1 in response.css('#competition-view-content ul li.singlemarkettype.onemarket '):
            itemtype = dict()
            dictionarylist = []
            if res1.css('.odds.markettable.table-hover.table .tbody .onemarket.tr'):
                for res2 in res1.css('.odds.markettable.table-hover.table .tbody .onemarket.tr'):
                    item = dict()
                    item['sports'] = response.meta['sports']
                    item['league'] = response.meta['league']
                    item['date'] = res2.css('.odds-th.res6.th span::attr(title)').extract_first().split('<br/>')[0]
                    item['time'] = res2.css('.odds-th.res6.th span::attr(title)').extract_first().split('<br/>')[1]
                    try:
                        item['FirstTeam'] = res2.css('.odds-th.res6.th a .ustop::text').extract_first().strip()
                    except:
                        item['FirstTeam'] = res2.css('.odds-th.res6.th a b::text').extract_first().split('v')[0]
                    try:
                        item['SecondTeam'] = res2.css('.odds-th.res6.th a .usbot::text').extract_first().strip()
                    except:
                        item['SecondTeam'] = res2.css('.odds-th.res6.th a b::text').extract_first().split('v')[1]
                    try:
                        item[f"Team1 {res1.css('.res2.th')[0].css('::text').extract_first()}"] = ' '.join(res2.css('.res2.td')[0].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[0].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[0].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team1 {res1.css(".res2.th")[1].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[1].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[1].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[1].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team1 {res1.css(".res2.th")[2].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[2].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[2].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[2].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    dictionarylist.append(item)
            else:
                for res2 in res1.css('.odds.markettable.table-hover.table.ustable .tbody .onemarket.tr'):
                    item = dict()
                    item['sports'] = response.meta['sports']
                    item['league'] = response.meta['league']
                    item['date'] = res2.css('.odds-th.res6.th span::attr(title)').extract_first().split('<br/>')[0]
                    item['time'] = res2.css('.odds-th.res6.th span::attr(title)').extract_first().split('<br/>')[1]
                    try:
                        item['FirstTeam'] = res2.css('.odds-th.res6.th a .ustop::text').extract_first().strip()
                    except:
                        item['FirstTeam'] = res2.css('.odds-th.res6.th a b::text').extract_first().split('v')[0]
                    try:
                        item['SecondTeam'] = res2.css('.odds-th.res6.th a .usbot::text').extract_first().strip()
                    except:
                        item['SecondTeam'] = res2.css('.odds-th.res6.th a b::text').extract_first().split('v')[1]
                    try:
                        item[f"Team1 {res1.css('.res2.th')[0].css('::text').extract_first()}"] = ' '.join(res2.css('.res2.td')[0].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[0].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[0].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team1 {res1.css(".res2.th")[1].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[1].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[1].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[1].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team1 {res1.css(".res2.th")[2].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[2].css('.tablebutton')[0].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    try:
                        item[f'Team2 {res1.css(".res2.th")[2].css("::text").extract_first()}'] = ' '.join(res2.css('.res2.td')[2].css('.tablebutton')[1].css(' ::text').extract()).strip().replace('\r\n', '')
                    except:
                        pass
                    dictionarylist.append(item)
            if dictionarylist.__len__() != 0:
                itemtype[res1.css('.panel-title span::text').extract_first('')] = dictionarylist
                items.append(itemtype)
        self.items.extend(items)

    def close(spider, reason):
        items_json_str = json.dumps(spider.items)
        fileout.write(items_json_str)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(intertopeu)
process.start()
