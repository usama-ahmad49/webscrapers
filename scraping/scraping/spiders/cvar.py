import csv
import string

import scrapy
from scrapy.crawler import CrawlerProcess

csvheaders = ['Name', 'FirstName', 'Lname', 'phone number', 'office number', 'fax', 'email', 'link']
file = open('data_CVAR.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(file, fieldnames=csvheaders)
writer.writeheader()


class CVAR(scrapy.Spider):
    name = 'sp'
    data = {'fulldetails': True, 'limit': 24, 'sortdirection': 'asc',
            'source': '@vroom-web/listing-1.3.7'}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '261',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'imssession=777096716; imslastConnect=1605266682164',
        'origin': 'https://ims.cvar.net',
        'pragma': 'no-cache',
        'referer': 'https://ims.cvar.net/scripts/mgrqispi.dll?APPNAME=IMS&PRGNAME=IMSMemberLogin&ARGUMENTS=-ACVAR&SessionType=N&ServiceName=OSRH&NotLogin=Y',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
    body = 'APPNAME=IMS&PRGNAME=IMSAgentsandOffices&ARGUMENTS=-A777096716%2C-N2%2CLastName%2C%28P%29+Agent+Nickname%2C%28P%29+Office+Name%2C%28P%29+City%2C%28P%29+Zip+Code&Search_Type=A&LastName={}&%28P%29+Agent+Nickname=&%28P%29+Office+Name=&%28P%29+City=&%28P%29+Zip+Code='

    def start_requests(self):
        l = [v for v in string.ascii_lowercase]
        for i in l:
            yield scrapy.Request('https://ims.cvar.net/scripts/mgrqispi.dll',
                                 body=self.body.format('{}'.format(i)), headers=self.headers, method='POST',
                                 meta={'letter': i})

    def parse(self, response):
        for link in [v for v in response.css('Table tr a::attr(href)').extract() if 'Agent' in v]:
            yield scrapy.Request('https://ims.cvar.net{}'.format(link), callback=self.parse_agent)
        if len([v for v in response.css('Table tr a::attr(href)').extract() if 'Agent' in v]) < 100:
            letter = response.meta['letter']

            last = response.css('Table a::text').extract()[-2][1]
            next_letter = chr(ord(last) + 1)
            yield scrapy.Request('https://ims.cvar.net/scripts/mgrqispi.dll',
                                 body=self.body.format('{}{}'.format(letter, next_letter)), headers=self.headers,
                                 method='POST',
                                 meta={'letter': letter})

    def parse_agent(self, response):

        item = dict()
        item['link'] = response.url
        s = response.css('table:nth-child(4) td::text').extract_first()
        item['Name'] = s
        full_name = s.split()
        item['FirstName'] = full_name[0]
        # if not x[2]:
        #     item['Lname']=x[1]
        # else:
        #     item['Lname']='{} {}'.format(x[1],x[2])

        item['Lname'] = (", ".join(repr(e) for e in full_name[1:])).replace("'", "")
        item['Lname'] = item['Lname'].strip().split()[-1]
        for tr in response.css('Table:nth-child(6) tr'):
            if 'Contact' in tr.css('td ::Text').extract()[0]:
                item['phone number'] = '1-{}'.format(
                    ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()]))
                item['phone number'] = item['phone number'] if len(item['phone number']) > 5 else ''
            if 'Office' in tr.css('td ::Text').extract()[0]:
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

process.crawl(CVAR)
process.start()
