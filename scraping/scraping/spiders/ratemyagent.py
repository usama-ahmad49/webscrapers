import csv
import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from AirtableApi import AirtableClient

header = ['Profile Id', 'Profile Url', 'City', 'city or suburb', 'Name', 'Phone Office', 'Phone Mobile', 'Agency', 'Agency Name', 'Agency Code', 'Agency Website']
fileout = open('ratemyagent.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=header)
writer.writeheader()
citynamelist = []


class ratemyagent(scrapy.Spider):
    name = 'ratemyagent'

    def start_requests(self):
        wikiresp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population')
        wikiresponce = scrapy.Selector(text=wikiresp.content.decode('utf-8'))
        for res in wikiresponce.css('#mw-content-text div.mw-parser-output table:nth-child(16) tbody tr')[2:]:
            name = ''.join(res.css('td:nth-child(2) ::text').extract()).strip()
            if '–' in name:
                n = name.split('–')
                citynamelist.append(n[0])
                citynamelist.append(n[1])
            else:
                citynamelist.append(name)
        for na in citynamelist:
            url = f'https://api.ratemyagent.com.au/AutoSearch/Locations?searchTerm={na}&skip=0&take=10'
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        city = data['Results'][0]['Name']
        for da in data['Results']:
            cityorsuburb = da['AutoSearchSubType']
            if da['Id'].isdigit():
                cityno = da['Id']
            else:
                cityno = da['Id'].split('-')[1]
            url = f'https://api.ratemyagent.com.au/Sales/Locations/Cities/{cityno}/Agents?StatisticType=TotalRecommendations&skip=0&take=10'
            page = requests.get(url=url)
            jsondata = json.loads(page.content.decode('utf-8'))
            totalResults = jsondata['Total']
            if totalResults < 600:
                newurl = f'https://api.ratemyagent.com.au/Sales/Locations/Cities/{cityno}/Agents?StatisticType=TotalRecommendations&skip=0&take=600'
                yield scrapy.Request(url=newurl, callback=self.parse_page, dont_filter=True, meta={'city': city, 'cityorsuburb': cityorsuburb})
            else:
                pg = totalResults / 600
                i = 1
                skip = 0
                if pg % 2 == 0:
                    while i <= int(pg):
                        newurl = f'https://api.ratemyagent.com.au/Sales/Locations/Cities/{cityno}/Agents?StatisticType=TotalRecommendations&skip={skip}&take=600'
                        skip += 600
                        i += 1
                        yield scrapy.Request(url=newurl, callback=self.parse_page, dont_filter=True, meta={'city': city, 'cityorsuburb': cityorsuburb})
                else:
                    while i <= (int(pg) + 1):
                        newurl = f'https://api.ratemyagent.com.au/Sales/Locations/Cities/{cityno}/Agents?StatisticType=TotalRecommendations&skip={skip}&take=600'
                        skip += 600
                        i += 1
                        yield scrapy.Request(url=newurl, callback=self.parse_page, dont_filter=True, meta={'city': city, 'cityorsuburb': cityorsuburb})
        else:
            pass

    def parse_page(self, response):
        data = json.loads(response.text)
        for da in data['Results']:
            item = dict()
            item['Profile Id'] = da['AgentProfileId']
            item['Profile Url'] = da['AgentProfileUrl']
            item['City'] = response.meta['city']
            item['city or suburb'] = response.meta['cityorsuburb']
            try:
                item['Name'] = da['Name']
            except:
                pass
            if da['Phone'] == '':
                try:
                    item['Phone Mobile'] = da['Mobile']
                except:
                    pass
            else:
                try:
                    item['Phone Office'] = da['Phone']
                except:
                    pass
                try:
                    item['Phone Mobile'] = da['Mobile']
                except:
                    pass
            try:
                item['Agency'] = da['Agency']['Name']
            except:
                pass
            try:
                item['Agency Name'] = da['Agency']['Name']
            except:
                pass
            try:
                item['Agency Code'] = da['Agency']['AgencyCode']
            except:
                pass
            try:
                item['Agency Website'] = da['Agency']['AgencyProfileUrl']
            except:
                pass
            writer.writerow(item)
            fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ratemyagent)
process.start()
