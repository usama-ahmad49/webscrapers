import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv
from copy import deepcopy
import datetime
import string

csvheaders = ['Name', 'FirstName', 'Lname', 'phone number', 'office number', 'fax', 'email', 'link']
file = open('data.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(file, fieldnames=csvheaders)
writer.writeheader()


class CSMAR(scrapy.Spider):
    name = 'sp'
    data = {'fulldetails': True, 'limit': 24, 'sortdirection': 'asc',
            'source': '@vroom-web/listing-1.3.7'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '261',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ga=GA1.2.1265779868.1604949562; _gid=GA1.2.1123785804.1604949562; _gat_gtag_UA_7682912_42=1; imssession=816662613; imslastConnect=1605028987409',
        'Host': 'ims.csmaor.com',
        'Origin': 'https://ims.csmaor.com',
        'Referer': 'https://ims.csmaor.com/scripts/mgrqispi.dll?APPNAME=IMS&PRGNAME=IMSMemberLogin&ARGUMENTS=-ACVAR&SessionType=N&ServiceName=OSRH&NotLogin=Y',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    body = 'APPNAME=IMS&PRGNAME=IMSAgentsandOffices&ARGUMENTS=-A816662613%2C-N2%2CLastName%2C%28P%29+Agent+Nickname%2C%28P%29+Office+Name%2C%28P%29+City%2C%28P%29+Zip+Code&Search_Type=A&LastName={}&%28P%29+Agent+Nickname=&%28P%29+Office+Name=&%28P%29+City=&%28P%29+Zip+Code='

    def start_requests(self):
        l = [v for v in string.ascii_lowercase]
        for i in l:
            yield scrapy.Request('https://ims.csmaor.com/scripts/mgrqispi.dll',
                                 body=self.body.format('{}'.format(i)), headers=self.headers, method='POST',
                                 meta={'letter': i})

    def parse(self, response):
        for link in [v for v in response.css('.table.table-striped tr a::attr(href)').extract() if 'Agent' in v]:
            yield scrapy.Request('https://ims.csmaor.com{}'.format(link), callback=self.parse_agent)
        if len([v for v in response.css('.table.table-striped tr a::attr(href)').extract() if 'Agent' in v]) < 100:
            letter = response.meta['letter']

            last = response.css('.table.table-striped a::text').extract()[-2][1]
            next_letter = chr(ord(last) + 1)
            yield scrapy.Request('https://ims.csmaor.com/scripts/mgrqispi.dll',
                                 body=self.body.format('{}{}'.format(letter, next_letter)), headers=self.headers,
                                 method='POST',
                                 meta={'letter': letter})

    def parse_agent(self, response):

        item = dict()
        item['link'] = response.url
        s = response.css('.memberName ::Text').extract_first('')
        item['Name'] = s
        x = s.split()
        item['FirstName'] = x[0]
        # if not x[2]:
        #     item['Lname']=x[1]
        # else:
        #     item['Lname']='{} {}'.format(x[1],x[2])

        item['Lname'] = (", ".join(repr(e) for e in x[1:])).replace("'", "")
        item['Lname'] = item['Lname'].strip().split()[-1]
        for tr in response.css('.table.table-striped tr'):
            if 'Phone Number' in tr.css('td ::Text').extract()[0]:
                item['phone number'] = '1-{}'.format(
                    ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()]))
                item['phone number'] = item['phone number'] if len(item['phone number']) > 5 else ''
            if 'Office Phone' in tr.css('td ::Text').extract()[0]:
                item['office number'] = '1- {}'.format(' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if
                                                                 v.strip()]))  # ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
            if 'Fax' in tr.css('td ::Text').extract()[0]:
                item['fax'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
                item['fax'] = '1-{}'.format(item['fax']) if item['fax'].strip() else ''
            if 'E-Mail' in tr.css('td ::Text').extract()[0]:
                item['email'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
        writer.writerow(item)
        file.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(CSMAR)
process.start()
