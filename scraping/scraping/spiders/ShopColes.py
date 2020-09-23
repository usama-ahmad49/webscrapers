import time
import scrapy
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class ShopColes(scrapy.Spider):
    name = 'shopcoles'
    title = 'ShopColes'
    # start_urls = ['https://shop.coles.com.au/a/brighton-bay-st/everything/browse']

    def start_requests(self):
        self.driver = webdriver.Ie()
        url='https://shop.coles.com.au/a/brighton-bay-st/everything/browse'
        self.driver.get(url)
        time.sleep(5)
        # =self.driver.page_source
        pageSource =scrapy.Selector(text=self.driver.page_source)
        for next in pageSource.css('.tile_colrsContentRecommendationWidget_Data_2_3074457345618260155_3074457345618340344_3 a[class="button button-rounded button-flat-red"] ::attr(href)').extract():
            next='https://shop.coles.com.au{}'.format(next)
            self.driver.get(next)
            prod=scrapy.Selector(text=self.driver.page_source)
            ColesProducts = prod.css('.product.product-new .product-main-info ').extract()
            for colesprod in ColesProducts:
                item = dict()
                item['Product-Brand'] = colesprod.css('span[role="text"] .product-brand ::text').extract()
                item['Product-Name'] = colesprod.css('span[role="text"] .product-name ::text').extract()
                item['Product-Price'] = colesprod.css(
                    '.product-pricing-info .dollar-value ::text').extract_first() + colesprod.css(
                    '.product-pricing-info .cent-value ::text').extract_first()
                item['Product-Size'] = colesprod.css('.package-size.accessibility-inline ::text').extract()
                item['Product-Unit-Price'] = colesprod.css('.package-price ::text').extract()
    #     yield scrapy.Request('https://shop.coles.com.au/a/brighton-bay-st/everything/browse')
    #
    # def parse(self, response):
    #     prodLinks = response.css('.heading-btn-container a::attr(href)').extract()
    #     for prodLink in prodLinks:
    #         yield scrapy.Request('https://shop.coles.com.au{}'.format(prodLink), callback=self.parse_products)
    #
    # def parse_products(self, response):
    #     prods = response.css('.product.product-new .product-main-info ').extract()
    #     for prod in prods:
    #         item = dict()
    #         item['Product-Brand'] = prod.css('span[role="text"] .product-brand ::text').extract()
    #         item['Product-Name'] = prod.css('span[role="text"] .product-name ::text').extract()
    #         item['Product-Price'] = prod.css('.product-pricing-info .dollar-value ::text').extract_first() + prod.css(
    #             '.product-pricing-info .cent-value ::text').extract_first()
    #         item['Product-Size'] = prod.css('.package-size.accessibility-inline ::text').extract()
    #         item['Product-Unit-Price'] = prod.css('.package-price ::text').extract()
