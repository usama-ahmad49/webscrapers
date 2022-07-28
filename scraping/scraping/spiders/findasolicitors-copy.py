import csv

import scrapy
from scrapy.crawler import CrawlerProcess

# header = ['Business Name', 'Address', 'Town', 'Postcode', 'Extra Postcode', 'Contact Name', 'Job Function', 'Job Title', 'Email Address', 'Full Telephone Number', 'Industry Directory Listing']
# fileoutEngland = open('findasolicitors - England.csv', 'w', newline='', encoding='utf-8')
# csvwriterEngland = csv.DictWriter(fileoutEngland, fieldnames=header)
# csvwriterEngland.writeheader()
# fileoutWales = open('findasolicitors - Wales.csv', 'w', newline='', encoding='utf-8')
# csvwriterWales = csv.DictWriter(fileoutWales, fieldnames=header)
# csvwriterWales.writeheader()
englandcount=0
walescount=0
englandndcount = 0
walesndcount = 0

class findasolicitors(scrapy.Spider):
    name = 'findasolicitors'
    def start_requests(self):
        for country in ['England', 'Wales']:
            for AOP in ['APL', 'PUB', 'ADV', 'AGR', 'AVI', 'BAN', 'BEN', 'CHA', 'CHI', 'CLI', 'COL', 'PCO', 'CCL', 'COS', 'COM', 'CON', 'CSU', 'CSF', 'CSG', 'CUT', 'CTR', 'PRE', 'CFI', 'CRD', 'CRF', 'CRG', 'CRJ', 'CRL', 'CRM', 'CRS', 'CRO', 'DEB', 'DTR', 'DEF', 'DRC', 'DRO', 'EDU', 'ELC', 'ELH', 'EMP', 'ENE', 'ENV', 'EUN', 'FDS', 'FAM', 'FAL', 'FMC', 'FME', 'FML', 'FPL', 'FIS', 'HRI', 'IMA', 'IML', 'IMM', 'IMG', 'IMN', 'ITE', 'INS', 'IUR', 'IPR', 'JRW', 'JRL', 'LCO', 'LRE', 'POA', 'LIC', 'LIV', 'LIS', 'LIT', 'LPH', 'LPP', 'MAR', 'MED', 'MHE', 'MHL', 'MAA', 'MIL', 'NDI', 'PEN', 'PIN', 'PIR', 'PLA', 'PRZ', 'PRP', 'PRT', 'PRW', 'PCI', 'PCP', 'PCT', 'PCW', 'PNE', 'TAX', 'TAC', 'TAE', 'TAH', 'TAM', 'TAP', 'TAT']:
                url = f'https://solicitors.lawsociety.org.uk/search/results?Type=0&IncludeNlsp=True&Location={country}&AreaOfPractice1={AOP}&Pro=True'
                yield scrapy.Request(url=url, meta={'country': country})

    def parse(self, response, **kwargs):
        totalresults = int(response.css('#main-content > div.search-results-controls > div:nth-child(2) > h1 > strong:nth-child(1)::text').extract_first().replace(',', ''))
        pages = totalresults / 20
        if pages.is_integer():
            pages = int(pages)
        else:
            pages = int(pages) + 1
        if pages > 30:
            pages = 30
        for i in range(1, pages + 1):
            url = response.url + f'&Page={i}'
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_data, meta={'country': response.meta['country']})

    def parse_data(self, response):
        for res in response.css('#results .solicitor.solicitor-type-firm'):
            url = 'https://solicitors.lawsociety.org.uk' + res.css('h2 a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_data_ind, meta={'country': response.meta['country']})

    def parse_data_ind(self, response):
        if response.meta['country'] == 'England':
            global englandcount, englandndcount
            if int(response.css('#people-and-structure-accordion > div:nth-child(1) > ul > li')[-1].css('a strong::text').extract_first()) == 1:
                englandcount +=1
            else:
                englandndcount +=1
        else:
            global walescount, walesndcount
            if int(response.css('#people-and-structure-accordion > div:nth-child(1) > ul > li')[-1].css('a strong::text').extract_first()) == 1:
                walescount += 1
            else:
                walesndcount += 1

    def close(spider, reason):
        fileopen = open('total firms and offices.txt', 'w')
        fileopen.write('England Companies with single offices: '+str(englandcount))
        fileopen.write('England Companies with multiple offices: '+str(englandndcount))
        fileopen.write('Wales Companies with single offices: '+str(walescount))
        fileopen.write('Wales Companies with multiple offices: '+str(walesndcount))
        fileopen.close()
        print(englandcount)
        print(englandndcount)
        print(walescount)
        print(walesndcount)
    #     item = dict()
    #     item['Business Name'] = response.css('#main-content > article > header > h1::text').extract_first()
    #     item['Address'] = ' '.join([v for v in response.css('#main-details-accordion dl') if v.css('dt::text').extract_first() == 'Address:'][0].css('dd::text').extract()).replace('\r\n', '').strip()
    #     item['Town'] = ' '.join([v for v in response.css('#main-details-accordion dl') if v.css('dt::text').extract_first() == 'Address:'][0].css('dd::text').extract()).replace('\r\n', '').strip().split(',')[-3].strip()
    #     item['Postcode'] = ' '.join([v for v in response.css('#main-details-accordion dl') if v.css('dt::text').extract_first() == 'Address:'][0].css('dd::text').extract()).replace('\r\n', '').strip().split(',')[-2].strip()
    #     if item['Address'].split(',')[-1].strip() != response.meta['country']:
    #         item['Extra Postcode'] = ' '.join(item['Address'].split(',')[-1].split()[1:])
    #         item['Address'] = item['Address'].replace(item['Extra Postcode'],'').strip()
    #     totalResults = int(response.css('#people-and-structure-accordion > div:nth-child(1) > ul > li:nth-child(1) > a > strong::text').extract_first())
    #     if totalResults > 20:
    #         pages = totalResults / 20
    #         if pages.is_integer():
    #             pages = int(pages)
    #         else:
    #             pages = int(pages) + 1
    #         for i in range(1, pages + 1):
    #             url = 'https://solicitors.lawsociety.org.uk' + response.css('#people-and-structure-accordion div:nth-child(1) ul li:nth-child(1) a::attr(href)').extract_first() + f'?Page={i}'
    #             yield scrapy.Request(url=url, callback=self.parse_data_people, meta={'dict': item, 'country': response.meta['country']})
    #     else:
    #         url = 'https://solicitors.lawsociety.org.uk' + response.css('#people-and-structure-accordion div:nth-child(1) ul li:nth-child(1) a::attr(href)').extract_first()
    #         yield scrapy.Request(url=url, callback=self.parse_data_people, meta={'dict': item, 'country': response.meta['country']})
    #
    # def parse_data_people(self, response):
    #     for res in response.css('#main-content .items section'):
    #         url = 'https://solicitors.lawsociety.org.uk' + res.css('header h2 a::attr(href)').extract_first().strip()
    #         yield scrapy.Request(url=url, callback=self.parse_data_people_ind, meta={'dict': response.meta['dict'], 'country': response.meta['country']})
    #
    # def parse_data_people_ind(self, response):
    #     item = response.meta['dict']
    #     item['Contact Name'] = response.css('#main-content > article > header > h1::text').extract_first()
    #     item['Job Function'] = ' and '.join(response.css('#main-details-accordion > div:nth-child(2) > dl > dd > ul > li::text').extract())
    #     item['Job Title'] = response.css('#main-content > article > header > p::text').extract_first('').strip()
    #     item['Email Address'] = response.css('#main-details-accordion .slidingDiv a::text').extract_first('')
    #     try:
    #         item['Full Telephone Number'] = '' if not ([v for v in response.css('#main-details-accordion .panel-half dl') if v.css('dt::text').extract_first() == 'Tel:'][0].css('dd::text').extract_first()).isdigit() else [v for v in response.css('#main-details-accordion .panel-half dl') if v.css('dt::text').extract_first() == 'Tel:'][0].css('dd::text').extract_first()
    #     except:
    #         item['Full Telephone Number'] = ''
    #     item['Industry Directory Listing'] = ''
    #     if response.meta['country'] == "England":
    #         csvwriterEngland.writerow(item)
    #         fileoutEngland.flush()
    #     elif response.meta['country'] == "Wales":
    #         csvwriterWales.writerow(item)
    #         fileoutWales.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(findasolicitors)
process.start()
