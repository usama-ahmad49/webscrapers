import csv

import scrapy
from scrapy.crawler import CrawlerProcess

headers = {
    'Host': 'www.amazon.es',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

csv_headers = ['product name', 'price', 'stars', 'available reviews', 'amount of reviews', 'product image', 'product description', 'related products', 'person name', 'stars', 'date', 'text of the review']
fileinput = open('amazonreviewbot.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileinput, fieldnames=csv_headers)
writer.writeheader()


class amazonreviewbot(scrapy.Spider):
    name = 'amazonreviewbot'

    def start_requests(self):
        url = 'https://www.amazon.es/s?k=monitores&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2'
        yield scrapy.Request(url=url, headers=headers)

    def parse(self, response, **kwargs):
        urllist = []
        for resp in response.css('.s-main-slot.s-result-list.s-search-results.sg-row .sg-col-inner'):
            try:
                url = 'https://www.amazon.es' + resp.css('.a-link-normal.s-no-outline::attr(href)').extract_first()
                urllist.append(url)
            except:
                pass
        for url in urllist:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_ind_product)

    def parse_ind_product(self, response):
        item = dict()
        rel_pro_link = []
        item['product name'] = response.css('#productTitle::text').extract_first().strip()
        item['price'] = response.css('#priceblock_ourprice::text').extract_first('').strip()
        item['stars'] = response.css('#reviewsMedley .a-fixed-left-grid-col.aok-align-center.a-col-right ::text').extract_first('zero stars')
        item['product image'] = ' || '.join(response.css('#altImages .a-spacing-small.item img::attr(src)').extract())
        item['product description'] = response.css('#productDescription p ::text').extract_first('').strip()
        for ress in response.css('#sp_detail li .a-section.sp_offerVertical.p13n-asin.sp_ltr_offer'):
            rel_pro_link.append(ress.css('a.a-link-normal')[0].css('::attr(href)').extract_first())
        item['related products'] = ' || '.join(rel_pro_link)
        reviewUrl = response.css('#cm-cr-global-review-list .a-link-emphasis.a-text-bold::attr(href)').extract_first()
        if reviewUrl != None:
            yield scrapy.Request(url='https://www.amazon.es' + reviewUrl + f'&pageNumber=1', headers=headers, callback=self.parse_ind_product_review, meta={'item': item})
        else:
            item['available reviews'] = 'non'
            writer.writerow(item)
            fileinput.flush()

    def parse_ind_product_review(self, response):
        i = int(response.url.split('&')[-1].split('=')[-1])
        newitem = response.meta['item']
        newitem['amount of reviews'] = response.css('#filter-info-section span::text').extract_first().strip().split('|')[0]
        for resp in response.css('#cm_cr-review_list .a-section.review.aok-relative'):
            newitem['person name'] = resp.css('.a-profile-name::text').extract_first()
            newitem['stars'] = resp.css('i[data-hook="review-star-rating"] ::text').extract_first()
            newitem['date'] = resp.css('span[data-hook="review-date"] ::text').extract_first().split('el')[1]
            newitem['text of the review'] = ' '.join(resp.css('span[data-hook="review-body"] ::text').extract()).strip()
            writer.writerow(newitem)
            fileinput.flush()
        if response.css('.a-pagination .a-last ::attr(href)').extract_first():
            i += 1
            url = response.url + f'&pageNumber={i}'
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_ind_product_review, meta={'item': response.meta['item']})


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(amazonreviewbot)
process.start()
