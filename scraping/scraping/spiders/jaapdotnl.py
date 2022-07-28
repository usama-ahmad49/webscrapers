import scrapy
import time
from selenium import webdriver
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.keys import Keys

class jaapdonl(scrapy.Spider):
    name = 'jaapdonl'

    def start_requests(self):
        urllist=[]
        driver=webdriver.Chrome()
        driver.get('https://www.jaap.nl/')
        # time.sleep(1)

        driver.find_element_by_id('didomi-notice-agree-button').click()
        driver.find_element_by_id('home-input').send_keys('Amsterdam')
        driver.find_element_by_id('home-input').send_keys(Keys.ENTER)
        time.sleep(3)
        # button=driver.find_element_by_id('submit-button')
        # button.submit()
        urllist.append(driver.current_url)
        for url in urllist:
            yield scrapy.Request(url=url, callback=self.parse_pages)
        driver.close()

    def parse_pages(self, response):
        total_pages=int(response.css('.result-content.navigation .page-info::text').extract_first().split()[3])
        i=1
        while i<=total_pages:
            yield scrapy.Request(url=response.url+'/p{}'.format(i), dont_filter=True,callback=self.parse_ind_url)
            i=i+1

    def parse_ind_url(self, response):
        for resp in response.css('.property-list .property a.property-inner'):
            url=resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = dict()
        item['streetAddress'] = response.css('.detail-address .detail-address-street::text').extract_first()
        item['zipCityAddress'] = response.css('.detail-address .detail-address-zipcity::text').extract_first()
        item['price'] = response.css('.detail-address .detail-address-price::text').extract_first().strip()
        item['image'] = response.css('.main-photo div')[1].css('::attr(style)').extract_first().split()[1].split('url(')[1].split(');')[0]
        item['description'] = ''.join(response.css('#long-description ::text').extract())
        item['type'] = ''


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(jaapdonl)
process.start()