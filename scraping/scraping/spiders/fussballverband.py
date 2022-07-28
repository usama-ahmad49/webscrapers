import csv
import psycopg2
import scrapy
from scrapy.crawler import CrawlerProcess

# header = ['team name', 'position', 'name', 'phone', 'email']
# fileout = open('fussballverband.csv', 'w', newline='', encoding='utf-8')
# writer = csv.DictWriter(fileout, fieldnames=header)
# writer.writeheader()
fileIn = open('Input_fussballverband.txt', 'r')
inputreader = fileIn.read().split('\n')
urllist = []

connection = psycopg2.connect(
                host = 'localhost',
                database = 'fussballverbanddb',
                user = 'postgres',
                password = '123456789',
                port='8080'
                )
cur = connection.cursor()
class fussballverband(scrapy.Spider):
    name = 'fussballverband'

    def start_requests(self):
        for url in inputreader:
            yield scrapy.Request(url)

    def parse(self, response, **kwargs):
        for url in response.css('#ctl01_ctl11_VereinMasterObject_ctl00_pnlVereine ul li a::attr(href)').extract():
            urllist.append(url + 'a-tr/')
            urllist.append(url + 'a-fu/')
        for url in urllist:
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        i = 0
        j = 2
        cur = connection.cursor()
        while i < 36:
            item = dict()
            item['team name'] = response.css('.panel.panel-default .navbar-brand ::text').extract_first()
            item['position'] = response.css('.row.heading')[i].css('div > h5 > div::text').extract_first()
            if item['position']==None:
                item['position'] = response.css('.row.heading')[i].css('div h5::text').extract_first()
            item['phone'] = ' || '.join(response.css(f'#ctl01_ctl11_VereinMasterObject_ctl01_tbResultate > div:nth-child({j}) a::text').extract())
            item['name'] = response.css('.ftName')[i].css('::text').extract_first()
            item['email'] = response.css(f'#ctl01_ctl11_VereinMasterObject_ctl01_tbResultate > div:nth-child({j})  div:nth-child(2) > div ::attr(src)').extract_first()

            cur.execute("INSERT INTO public.fussballverbandtable(teamname, position, name, phone, email) VALUES ('" +
            item['team name'] + "', '" + item['position'] + "', '" + item['name'] + "', '" +item['phone'] + "', '" + item[
            'email'] + "')")
            connection.commit()
            # writer.writerow(item)
            # fileout.flush()
            i = i + 1
            j = j + 2
        connection.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(fussballverband)
process.start()
