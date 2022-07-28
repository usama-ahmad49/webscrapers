import scrapy
import json
import requests
from scrapy.crawler import CrawlerProcess

citylist = []
class woltdotcom(scrapy.Spider):
    name = 'woltdotcom'

    def start_requests(self):
        link = "https://en.wikipedia.org/wiki/List_of_most_populous_cities_in_Kazakhstan"
        resp = requests.get(link)
        res = scrapy.Selector(text=resp.content.decode('utf-8'))
        for re in res.css('.wikitable.sortable tr')[1:]:
            citylist.append(re.css('td a')[0].css('::Text').extract_first().lower())
        for city in citylist:
            # url =f"https://restaurant-api.wolt.com/v1/pages/front/{city}"
            url = 'https://wolt.com/en/kaz/shymkent/restaurant/bullki-tauke-khan'
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        Jdata = json.loads(response.text)
        for data in Jdata['sections'][1:-1]:
            for da in data['items']:
                picture = da['image']['url']
                link = "https://restaurant-api.wolt.com"+da['link']['target']
                yield scrapy.Request(url=link, callback=self.parsedata, meta={'picture':picture})

    def parsedata(self, response):
        Jdata = json.loads(response.text)
        for data in Jdata['sections']:
            for da in data:
                pass
process = CrawlerProcess({'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})
process.crawl(woltdotcom)
process.start()
