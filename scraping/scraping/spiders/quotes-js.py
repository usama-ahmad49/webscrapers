import scrapy
from scrapy_splash import SplashRequest


class QuotesJsSpider(scrapy.Spider):
    name = 'quotesjs'

    # start_urls=['http://quotes.toscrape.com/js']
    def start_requests(self):
        yield SplashRequest(
            url="http://quotes.toscrape.com/js/",
            callback=self.parse,
        )

    def parse(self, response):
        for quote in response.css("div.quote"):
            item=dict()
            item['text']= quote.css("span.text::text").extract_first()
            # yield {
            #     'text': quote.css("span.text::text").extract_first(),
            #     'author': quote.css("small .author::text").extract_first(),
            #     'tags': quote.css(".tags a::text").extract(),
            # }
            print('lalalala')
            yield item
