import csv
from selenium import webdriver
import scrapy
from scrapy.crawler import CrawlerProcess

header = ["Business Name","Phone","Address",  "Website", "Rating", "Review Count",]
fileout = open('Home Advisor Scraper - Output Sheet.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=header)
writer.writeheader()


class homeadvisor(scrapy.Spider):
    name = 'homeadvisor'

    def start_requests(self):
        urllist=[]
        driver=webdriver.Firefox()
        driver.get('https://www.homeadvisor.com/c.TX.html')
        fileinput = open('Home Advisor Scraper - Input Sheet.csv', 'r')
        inputlist = fileinput.read()
        for zip in inputlist.split('\n')[1:]:
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/select/option[11]').click()
            driver.find_element_by_id('zip').send_keys(zip)
            driver.find_element_by_xpath('//*[@id="xl-change-service"]').click()
            urllist.append(driver.current_url)
            driver.get('https://www.homeadvisor.com/c.TX.html')
        driver.close()
        for url in urllist[:-1]:
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response):
        pages=int(response.css('.xmd--pagination.pagination-bottom .xmd--pagination_right span::text').extract_first().split('of ')[1])
        i=1
        el = 0
        yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
        while i<pages:
            url = response.url + '&startingIndex={}'.format(el + 25)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse)
            el = el + 25
            i=i+1

    def parse(self, response):
        for resp in response.css('.sp_card-inner')[:-1]:
            item = dict()
            item['Business Name'] = resp.css('.sp-description a::text').extract_first()
            item['Phone'] = resp.css('.telephone-number::text').extract_first()
            url='https://www.homeadvisor.com' + resp.css('.sp-description a::attr(href)').extract_first()
            item['Website'] = 'https://www.homeadvisor.com' + resp.css('.sp-description a::attr(href)').extract_first()
            item['Rating'] = resp.css('.numeric-rating::text').extract_first()
            try:
                item['Review Count'] = resp.css('.verified-reviews a::text').extract_first().split('\n')[0]
            except:
                item['Review Count'] = ''
            yield scrapy.Request(url=url, callback=self.get_address, meta={'Business Name': item['Business Name'], 'Phone': item['Phone'], 'Website': item['Website'], 'Rating': item['Rating'], 'Review Count': item['Review Count']})

    def get_address(self, response):
        item2 = dict()
        if response.css('#details address ::text').extract_first():
            item2['Address'] = ''.join(response.css('#details address ::text').extract())
        else:
            item2['Address'] = ', '.join(v for v in response.css('.sp-address ::text').extract() if '\n' not in v)
        item2['Phone'] = response.meta['Phone']
        item2['Website'] = response.meta['Website']
        item2['Rating'] = response.meta['Rating']
        item2['Review Count'] = response.meta['Review Count']
        item2['Business Name'] = response.meta['Business Name']
        writer.writerow(item2)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(homeadvisor)
process.start()
