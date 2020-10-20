try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass


from scrapy.crawler import CrawlerProcess
import scrapy
import csv

header=['Yard City', 'Year', 'Make', 'Model', 'Manufacturer', 'Color', 'Yard Date', 'Row', 'Vin','Check Vin url','Contact url']
file=open('WeGotUseddotCom.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(file,fieldnames=header)
writer.writeheader()
class WeGotUseddotCom(scrapy.Spider):
    name = 'wegotuseddotcom'
    title = 'WeGotUseddotCom'
    def start_requests(self):
        pge=0
        while pge<175: #174 pages have stored results in them
            yield scrapy.Request('https://wegotused.com/our-inventory/?inv[yard]=HAZLE%20TOWNSHIP&inv[make]=&inv[model]=&inv[manufacturer]=&inv[year]=&inv[part]=&inv[page]={}&inv[sort][yard_date]=0&inv[sort][yard_city]=1'.format(pge))
            pge=pge+1



    def parse(self, response):
        item=dict()
        # pge=response.meta['pge']+1
        # if not response.css('#post-10 .results tbody tr'):
        #     yield item
        for resp in response.css('#post-10 .results tbody tr'):
            item['Yard City'] = resp.css('td:nth-child(1)::text').extract_first()
            item['Year'] = resp.css('td:nth-child(2)::text').extract_first()
            item['Make'] = resp.css('td:nth-child(3)::text').extract_first()
            item['Model'] = resp.css('td:nth-child(4)::text').extract_first()
            item['Manufacturer'] = resp.css('td:nth-child(5)::text').extract_first()
            item['Color'] = resp.css('td:nth-child(6)::text').extract_first()
            item['Yard Date'] = resp.css('td:nth-child(7)::text').extract_first()
            item['Row'] = resp.css('td:nth-child(8)::text').extract_first()
            item['Vin'] = resp.css('td:nth-child(9)::text').extract_first()
            item['Check Vin url']=resp.css('td:nth-child(10) .btn.btn-sm.yellow.text-dark::attr(href)').extract_first()
            item['Contact url']='https://wegotused.com'+resp.css('td:nth-child(10) .btn.btn-sm.teal.text-light::attr(href)').extract_first()
            writer.writerow(item)
            file.flush()

        # yield scrapy.Request('https://wegotused.com/our-inventory/?inv[yard]=HAZLE%20TOWNSHIP&inv[make]=&inv[model]=&inv[manufacturer]=&inv[year]=&inv[part]=&inv[page]={}&inv[sort][yard_date]=0&inv[sort][yard_city]=1'.format(pge), callback=self.parse, meta={'pge':pge})
        yield item

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(WeGotUseddotCom)
process.start()
