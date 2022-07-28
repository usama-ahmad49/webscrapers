import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

headers_csv=['name','seller rank']
fileout=open('amazonbooksearch.csv','w', newline='', encoding='utf-8')
writer=csv.DictWriter(fileout,fieldnames=headers_csv)
writer.writeheader()


fileinput = open('inputAmazonbooksearch.txt', 'r', encoding='utf-8')
inputstring = fileinput.read().split('\n')
options = Options()
options.headless = True

class amazonbooksearch(scrapy.Spider):
    name = 'amazonbooksearch'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 5,
    }

    def start_requests(self):
        driver = webdriver.Firefox(options=options)
        for inputstr in inputstring:
            url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'.format('+'.join(inputstr.split()))
            driver.get(url=url)
            req = [v for v in driver.requests if 'https://www.amazon.com/s?k=' in v.url][0]
            headers = dict(req.headers)
            yield scrapy.Request(url=url, headers=headers, meta={'inputstr': inputstr})
        driver.close()

    def parse(self, response, **kwargs):
        browser = webdriver.Firefox(options=options)
        for resp in response.css('.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.sg-col-12-of-16'):
            if ' '.join(response.meta['inputstr'].split()[:-1]) in resp.css('.a-size-medium.a-color-base.a-text-normal::text').extract_first():
                url = 'https://www.amazon.com' + resp.css('.a-link-normal.a-text-normal::attr(href)').extract_first()
                if 'audiobook'not in url:
                    browser.get(url=url)
                    browser.find_element_by_xpath('//*[@id="tmmSwatches"]/ul/li[1]').click()
                    url=browser.current_url
                break
        browser.get(url=url)
        requ = [v for v in browser.requests if 'https://www.amazon.com/' in v.url][0]
        headers = dict(requ.headers)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_book, meta={'inputstr':response.meta['inputstr']})
        browser.close()

    def parse_book(self, response, **kwargs):
        pass
        item=dict()
        item['name'] = response.meta['inputstr']
        for resp in response.css('#audibleproductdetails_feature_div table tr'):
            if 'Sellers Rank' in resp.css('th::text').extract_first():
                item['seller rank'] = (resp.css('td span span::text').extract_first().split()[0]).replace('#','')
                break
        writer.writerow(item)
        fileout.flush()




process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(amazonbooksearch)
process.start()
