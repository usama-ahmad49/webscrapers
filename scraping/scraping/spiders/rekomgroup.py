import scrapy
import csv
from scrapy.crawler import CrawlerProcess
import json

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('rekomgroup.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()
class rekomgroup(scrapy.Spider):
    name = 'rekomgroup'

    def start_requests(self):
        url = 'https://www.rekomgroup.com/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        jstr = [v for v in response.css('script[type="text/javascript"]::text').extract() if 'wpgmaps_custom_cluster_options' in v][0].split('wpgmaps_localize_marker_data =')[-1].split('};')[0]+'}'
        jdata = json.loads(jstr)
        allkeys = list(jdata['1'].keys())
        for key in allkeys:
            item = dict()
            item['Venue Group'] = 'rekomgroup'
            item['Venue Name'] = jdata['1'][key]['title']
            item['Full Address'] = jdata['1'][key]['address']
            if jdata['1'][key]['address'].split(',').__len__() > 2:
                item['City'] = jdata['1'][key]['address'].split(',')[-2]
                item['Country'] = jdata['1'][key]['address'].split(',')[-1]
            else:
                item['City'] = jdata['1'][key]['address'].split(',')[-1]
            if jdata['1'][key]['address'].split(',').__len__() ==1:
                item['City'] = ' '.join(jdata['1'][key]['address'].split()[-2:])
            csvwriter.writerow(item)
            fileinputcsv.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(rekomgroup)
process.start()
