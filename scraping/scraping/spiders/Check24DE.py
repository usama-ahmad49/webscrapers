try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv

import scrapy
from scrapy.crawler import CrawlerProcess


csvfileR=open('zip_codes.csv','r',encoding='utf-8')
input_reader=csvfileR.read()

csv_columns = ["zipcode","city","street","Primary Provider_Name","Primary Provider Rate_Name","Arbeitspreis pro kWh brutto","Arbeitspreis pro kWh (netto)","Grundpreis brutto","Grundpreis (netto)","Rate Version","Rate Version Date"]
csvfileW = open('Output_Check24.csv','w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfileW, fieldnames=csv_columns)
writer.writeheader()


class Check24DE(scrapy.Spider):
    name = 'Check'
    title = 'Check'
    start_urls = ['https://www.check24.de/strom/']

    def start_requests(self):
        for data in input_reader.split('\n')[1:]:
            list=data.split(',')

            city=list[1]
            zipcode=int(list[0])
            street=list[2]

            url='https://www.check24.de/strom/vergleich/check24/?zipcode={}&city={}&street={}&calculationparameter_id=f3675085d6661c3b3bba4bcedb95ca36'.format(zipcode,city,street)
            yield scrapy.Request(url, meta={'city':city, 'zipcode':zipcode, 'street': street})

    def parse(self, response):
        item=dict()

        item['zipcode']=response.meta['zipcode']
        item['city']=response.meta['city']
        item['street']=response.meta['street']



        item['Primary Provider_Name']=response.css('#reference_provider_hash option[selected="selected"]::text').extract_first()
        item['Primary Provider Rate_Name']=response.css('#reference_tariffversion_key option[selected="selected"]::text').extract_first()
        for row in response.css('.filter-section .pricelayer-table .pricelayer-table__row'):
            if 'arbeitspreis pro' in row.css('.pricelayer-table__label ::text').extract_first('').strip().lower():
                Arbeitspreis=row.css('.pricelayer-table__value ::text').extract_first('').strip().split()
                Abrutto=Arbeitspreis[0]
                ANetto=Arbeitspreis[1]
                item['Arbeitspreis pro kWh brutto'] = Abrutto.replace("\n'", "")
                item['Arbeitspreis pro kWh (netto)'] = ANetto.replace("\n'()", "")

            if 'grundpreis' in row.css('.pricelayer-table__label ::text').extract_first('').strip().lower():
                grund=row.css('.pricelayer-table__value ::text').extract_first('').strip().split()
                Gbrutto=grund[0]
                Gnetto=grund[1]
                item['Grundpreis brutto']=Gbrutto.replace("\n'", "")
                item['Grundpreis (netto)']=Gnetto.replace("\n'()", "")

        Rate=response.css('.ajax-pricelayer__text::text').extract()
        version=Rate[1].strip().split()
        item['Rate Version']=version[1].replace(",","")
        item['Rate Version Date']=version[4][:10]

        writer.writerow(item)
        csvfileW.flush()
        yield item


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Check24DE)
process.start()
