import json
import requests
from copy import deepcopy
import sys
import csv
from os import listdir
from os.path import isfile, join
import scrapy
from scrapy.crawler import CrawlerProcess

csv.field_size_limit(sys.maxsize)

path = 'E:/Project/pricescraperlk/scraping/scraping/spiders/esco-bundle(6)/v1.1.0'   #"Enter Folder Path"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and '.csv' in join(path, f)]
class europadoteu(scrapy.Spider):
    name = 'europadoteu'
    def start_requests(self):
        for file in onlyfiles:
            filewrite = open('new_' + file, 'w', encoding='utf-8', newline='')
            fileopen = open(path+'/'+file, 'r', encoding='utf-8')

            reader = csv.DictReader(fileopen)
            headers = reader.fieldnames
            headers = headers+['Code_new', 'Title_new', 'Description_new', 'Alternative Labels_new', 'Essential Skills & Competences_new', 'Essential Knowledge_new', 'Optional Skills & Competences_new', 'Optional Knowledge_new']
            csvwriter = csv.DictWriter(filewrite, fieldnames=headers)

            if filewrite.tell() == 0:
                csvwriter.writeheader()
            for row in reader:
                url = row[list(row.keys())[1]]
                if url !='' and 'data.europa.eu/esco' in url:
                    yield scrapy.Request(url='https://esco.ec.europa.eu/en/classification/occupation?uri='+row[list(row.keys())[1]], callback= self.parse, meta={'allData':row,'filename':file, 'writer': csvwriter, 'fileobj':filewrite})
                    # yield scrapy.Request(url='https://esco.ec.europa.eu/en/classification/occupation?uri=http%3A%2F%2Fdata.europa.eu%2Fesco%2Foccupation%2F000e93a3-d956-4e45-aacb-f12c83fedf84', callback= self.parse, meta={'allData':row,'filename':file, 'writer': csvwriter, 'fileobj':filewrite})
                else:
                    item = dict()
                    for i in range (0,list(row.keys()).__len__()):
                        item[list(row.keys())[i]] = row[list(row.keys())[i]]
                        csvwriter.writerow(item)
                        filewrite.flush()


    def parse(self, response, **kwargs):
        item = response.meta['allData']
        item['Code_new'] = response.css('#description > div.code > p:nth-child(2)::text').extract_first('')
        item['Title_new'] = response.css('#block-mainpagecontent h3::text').extract_first('').strip()
        item['Description_new'] =response.css('#description > div.description > p:nth-child(2)::text').extract_first('')
        item['Alternative Labels_new'] = '' if len(response.css('.alternative-label-item::text').extract()) ==0 else '; '.join(response.css('.alternative-label-item::text').extract())
        item['Essential Skills & Competences_new'] = '' if len(response.css('#essential-skills-list a::text').extract()) == 0 else '; '.join(response.css('#essential-skills-list a::text').extract())
        item['Essential Knowledge_new'] = '' if len(response.css('#essential-knowledge-list a::text').extract()) == 0 else '; '.join(response.css('#essential-knowledge-list a::text').extract())
        item['Optional Skills & Competences_new'] = '' if len(response.css('#optional-skills-list a::text').extract()) == 0 else '; '.join(response.css('#optional-skills-list a::text').extract())
        item['Optional Knowledge_new'] = '' if len(response.css('#optional-knowledge-list a::text').extract()) == 0 else '; '.join(response.css('#optional-knowledge-list a::text').extract())
        response.meta['writer'].writerow(item)
        response.meta['fileobj'].flush()
        # csvwriter.writerow(item)
        # filewrite.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(europadoteu)
process.start()