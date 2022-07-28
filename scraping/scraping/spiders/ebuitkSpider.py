import scrapy
import shopify
from scrapy.crawler import CrawlerProcess

APIKey = "1db1b32be18891082b702cf43ecb09d0"
APIKeyPassword = "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"
SharedSecret = "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"

string = f"https://{APIKey}:{APIKeyPassword}@oxka.myshopify.com/admin/api/2020-10/orders.json"
# shopify.Session.setup(api_key=APIKey, secret=APIKeyPassword)
shop_url = "oxka.myshopify.com"
api_version = '2020-10'
# state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
# redirect_uri = "http://myapp.com/auth/shopify/callback"
# scopes = ['read_products', 'read_orders','write_products']
#
# newSession = shopify.Session(shop_url, api_version)
# auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
# # redirect to auth_url
#
# session = shopify.Session(shop_url, api_version)
# access_token = session.request_token(request_params) # request_token will validate hmac and timing attacks
# # you should save the access token now for future use.

# session = shopify.Session(shop_url, api_version, APIKeyPassword)
# shopify.ShopifyResource.activate_session(session)


# ...
# shopify.ShopifyResource.clear_session()
auth = shopify.OAuthHandler(APIKey, APIKeyPassword)

class ebutikSpider(scrapy.Spider):
    name = 'ebutikspider'
    # session = shopify.Session(shop_url, api_version, APIKeyPassword)
    # shopify.ShopifyResource.activate_session(session)
    def start_requests(self):
        url = 'https://ebutik.pl/'
        yield scrapy.Request(url=url)

    def parse(self, response):
        for resp in response.css('#menu_categories .navbar-collapse .navbar-subnav.active li .navbar-subsubnav a'):
            category_url = 'https://ebutik.pl'+resp.css('::attr(href)').extract_first()
            category_name = resp.css('::text').extract_first()
            # collect = shopify.Collect({'custom_collection': {'title': category_name}})
            # collect.save()
            yield scrapy.Request(url=category_url, callback=self.parse_item)

    def parse_item(self, response):
        for resp in response.css('#search .product_wrapper.col-12.col-md-3.col-sm-4'):
            item = dict()
            item['Name'] = resp.css('h3 a.product-name::text').extract_first()
            item['max_price'] = resp.css('.product_prices .max-price::text').extract_first()
            item['price'] = resp.css('.product_prices .price::text').extract_first()
            item['url'] = resp.css('.product_icon_wrapper .product-icon.align_row::attr(href)').extract_first()
            sizes = resp.css('.search_details .sizes_wrapper span::text').extract()  # check if it has small size then put yes for all sizes
            # if 'S' in sizes:
            #     item['size_small'] = true
            new_product = shopify.Product({'product': {'title': item['Name'], 'options': [{'name': 'size', 'values': [{'0': sizes[0], '1': sizes[1]}]}], 'max_price': item['max_price'], 'price': item['price'], 'images': 'images url'}})
            new_product.save()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ebutikSpider)
process.start()
