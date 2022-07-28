import scrapy
from scrapy.crawler import CrawlerProcess
import selenium
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    url = 'https://www.reddit.com/r/funny/comments/nzp2n0/announcement_were_making_some_changes_to_how/'
    driver.get(url)
    print('this is a comment')


# class reddit(scrapy.Spider):
#     name = 'reddit'
#     def start_requests(self):
#         url = 'https://www.reddit.com/r/funny/comments/nzp2n0/announcement_were_making_some_changes_to_how/'
#         yield scrapy.Request(url=url)
#     def parse(self, response,**kwargs):
#         pass
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
# process.crawl(reddit)
# process.start()
