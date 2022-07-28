import scrapy
from scrapy.crawler import CrawlerProcess


class redfin(scrapy.Spider):
    name = 'redfin'
    # custom_settings = {
    #     'CLOSESPIDER_PAGECOUNT': 500,
    #     'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
    #     'CRAWLERA_ENABLED': True,
    #     'CRAWLERA_APIKEY': '34f4cde68cf14c9f884dacf894fa670f',
    #     'AUTOTHROTTLE_ENABLED': False,
    #     # 'CONCURRENT_REQUESTS': 1,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    #     'DOWNLOAD_TIMEOUT': 600,
    #     'DOWNLOAD_DELAY': 0.3,
    #     'RETRY_TIMES': 10,
    #     'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
    #     # 'HTTPCACHE_ENABLED': True,
    #     # 'HTTPCACHE_DIR': 'D:\cache'
    # }
    Rfile = open('input_zillow.txt', 'r')
    inputfile = Rfile.read()
    links = inputfile.split('\n')
    links = [z for z in links if z.strip()]

    def start_requests(self):
        for zip in self.links:
            url = f'https://www.redfin.com/zipcode/{zip}'
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(redfin)
process.start()
