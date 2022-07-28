import csv
import json

import scrapy
from scrapy.crawler import CrawlerProcess

# import odooApi
# from currency_converter import CurrencyConverter
# c = CurrencyConverter()

# odooClient = odooApi.odooClient()

headers_csv = ['brand', 'name_en', 'gender', 'color', 'size', 'group_sku', 'product_sku', 'description_en',
               'main_category', 'category', 'sub_category', 'base_category', 'material', 'origin', 'size_slug',
               'description_plain_en', 'delivery_information', 'variation_type', 'serial_no', 'strike_through_price',
               'original_price', 'whole_sale_price', 'retail_price', 'main_pic',

               "image_1", "image_2", "image_3", "image_4", "image_5", "image_6", "image_7", "image_8", "image_9",
               "image_10", "image_11", "image_12", "image_13", "image_14", "image_15", "image_16", "image_17",
               "image_18", "image_19", "image_20", "image_21", "image_22", "image_23", "image_24", "image_25",
               "image_26", "image_27", "image_28", "image_29", "image_30", "image_31", "image_32", "image_33",
               "image_34", "image_35", "image_36",

               "variant_1", "variant_1_price", "variant_2", "variant_2_price",
               "variant_3", "variant_3_price", "variant_4", "variant_4_price", "variant_5", "variant_5_price",
               "variant_6", "variant_6_price", "variant_7", "variant_7_price", "variant_8", "variant_8_price",
               "variant_9", "variant_9_price", "variant_10", "variant_10_price", "variant_11", "variant_11_price",
               "variant_12", "variant_12_price", "variant_13", "variant_13_price", "variant_14", "variant_14_price",
               "variant_15", "variant_15_price", "variant_16", "variant_16_price", "variant_17", "variant_17_price",
               "variant_18", "variant_18_price", "variant_19", "variant_19_price", "variant_20", "variant_20_price",
               "variant_21", "variant_21_price", "variant_22", "variant_22_price", "variant_23", "variant_23_price",
               "variant_24", "variant_24_price", "variant_25", "variant_25_price", "variant_26", "variant_26_price",
               "variant_27", "variant_27_price", "variant_28", "variant_28_price", "variant_29", "variant_29_price",
               "variant_30", "variant_30_price", "variant_31", "variant_31_price", "variant_32", "variant_32_price",
               "variant_33", "variant_33_price", "variant_34", "variant_34_price", "variant_35", "variant_35_price",
               "variant_36", "variant_36_price", "variant_37", "variant_37_price", "variant_38", "variant_38_price",
               "variant_39", "variant_39_price", "variant_40", "variant_40_price", "variant_41", "variant_41_price",
               "variant_42", "variant_42_price", "variant_43", "variant_43_price", "variant_44", "variant_44_price",
               "variant_45", "variant_45_price", "variant_46", "variant_46_price", "variant_47", "variant_47_price",
               "variant_48", "variant_48_price", "variant_49", "variant_49_price", "variant_50", "variant_50_price",
               "variant_51", "variant_51_price", "variant_52", "variant_52_price", "variant_53", "variant_53_price",
               "variant_54", "variant_54_price", "variant_55", "variant_55_price", "variant_56", "variant_56_price",
               "variant_57", "variant_57_price", "variant_58", "variant_58_price", "variant_59", "variant_59_price",
               "variant_60", "variant_60_price", "variant_61", "variant_61_price", "variant_62", "variant_62_price",
               "variant_63", "variant_63_price", "variant_64", "variant_64_price", "variant_65", "variant_65_price",
               "variant_66", "variant_66_price", "variant_67", "variant_67_price", "variant_68", "variant_68_price",
               "variant_69", "variant_69_price", "variant_70", "variant_70_price", "variant_71", "variant_71_price",
               "variant_72", "variant_72_price", "variant_73", "variant_73_price", "variant_74", "variant_74_price",
               "variant_75", "variant_75_price", "variant_76", "variant_76_price", "variant_77", "variant_77_price",
               "variant_78", "variant_78_price", "variant_79", "variant_79_price", "variant_80", "variant_80_price",
               "variant_81", "variant_81_price", "variant_82", "variant_82_price", "variant_83", "variant_83_price",
               "variant_84", "variant_84_price", "variant_85", "variant_85_price", "variant_86", "variant_86_price",
               "variant_87", "variant_87_price", "variant_88", "variant_88_price", "variant_89", "variant_89_price",
               "variant_90", "variant_90_price", "variant_91", "variant_91_price", "variant_92", "variant_92_price",
               "variant_93", "variant_93_price", "variant_94", "variant_94_price", "variant_95", "variant_95_price",
               "variant_96", "variant_96_price", "variant_97", "variant_97_price", "variant_98", "variant_98_price",
               "variant_99", "variant_99_price", "variant_100", "variant_100_price"
               ]
# colnames = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
#             'name_en','strike_through_price', "original_price",'retail_price', 'whole_sale_price', 'description_en', 'main_pic', 'pic1', 'pic2', 'pic3', 'pic4', 'pic5', 'gender',
#             'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
#             'description_plain_en', 'delivery_information', 'badges_en', 'additional_categories', 'restrict_payment', 'meta_title_en',
#             'meta_keyword_en', 'meta_description_en', 'status', 'operation', 'state', 'image_thumbnails', 'search_terms', 'website_ids',
#             'product_tmpl_id', 'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_date_deadline', 'activity_summary',
#             'activity_exception_decoration', 'activity_exception_icon', 'message_is_follower', 'message_follower_ids','message_partner_ids',
#             'message_channel_ids', 'message_ids', 'message_unread', 'message_unread_counter', 'message_needaction', 'message_needaction_counter',
#             'message_has_error', 'message_has_error_counter', 'message_main_attachment_id', 'website_message_ids', 'message_has_sms_error',
#             'message_attachment_count', 'id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date', '__last_update']

required_keys = ['group_sku', 'product_sku', 'brand', 'name_en', 'whole_sale_price', 'description_en', 'main_pic', 'pic1', 'gender', 'main_category', 'category', 'sub_category', 'base_category',
                 'size', 'color', 'material', 'origin', 'size_slug', 'description_plain_en', 'delivery_information']
# processed = []
vendor = 'slamjam'
fileout = open('slamjam.csv', mode='w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()


class slamjam(scrapy.Spider):
    name = 'slamjam'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_TIMEOUT': 1000,
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [302, 503],

        'ROTATING_PROXY_LIST_PATH': 'E:\Project\pricescraperlk\scraping\scraping\spiders\proxy.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        }
        # 'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        # 'CRAWLERA_ENABLED': True,
        # 'CRAWLERA_APIKEY': 'c29fb925abf7499ea97801bc05ce2863',
    }
    headers = {
        "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en - US, en;q = 0.9",
        "cache-control": "no-cache",
        "cookie": 'cqcid=abAsIISGO5YOOXgYjyxPx5zUaZ; cquid=||; dwanonymous_45aa0f5b66c2339d1f2dbcca0394a60d=abAsIISGO5YOOXgYjyxPx5zUaZ; __cq_dnt=0; dw_dnt=0; _ga=GA1.2.526118371.1627628076; _fbp=fb.1.1627628078082.1981863360; __cq_uuid=abt1X8S38pG0BRzGTNsls092kM; consentTrackingCookie=1; cf_clearance=0b281fb1071b88ebe71ab77b2900957a2dd9a9f3-1627914235-0-150; datadome=NcA-y5eRGF97t-G0dCgj~0g9Bv1XWp6ar8X3TMjuj4bZ7~~Au_XfGdl5BPPjjqFlqhJ4rmR_9dHNP7xQZMrkjZAyXVshX6dG8e1~n-EjoJ; __cq_bc=%7B%22bdhr-slamjam%22%3A%5B%7B%22id%22%3A%22AV2187%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J217885%22%7D%2C%7B%22id%22%3A%221021A161%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J151243%22%7D%2C%7B%22id%22%3A%22A07FW732%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J220572%22%7D%2C%7B%22id%22%3A%22DD0060%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J220111%22%7D%2C%7B%22id%22%3A%22DH3718%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J222517%22%7D%2C%7B%22id%22%3A%22DB4612%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J203107%22%7D%2C%7B%22id%22%3A%2227316201%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J223081%22%7D%2C%7B%22id%22%3A%2227207001%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J223080%22%7D%2C%7B%22id%22%3A%220121308001001%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J229307%22%7D%2C%7B%22id%22%3A%22CN7841%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%22J129386%22%7D%5D%7D; dwac_496bb2c3f69aa0ccb6fd3f42c4=YO2_GaP4O35GiUfZ5nRo-iBD_SbMj1zpLgE%3D|dw-only|||EUR|false|Europe%2FRome|true; sid=YO2_GaP4O35GiUfZ5nRo-iBD_SbMj1zpLgE; dwsid=s1PRdGH6PtWin53YdnXW0_P9k0sOjVlCyhc7sJ53uRmHylNttgDUEkUcAW2an63WdjkX1D0XqyINL1etktummQ==; __cf_bm=0c53de6613f142484b7784e5aa5bbe28eb848eda-1629894098-1800-Ab+7knvICcv+xc3KvYGcV9OiZl/0WNlPtyNOZf0Yl0Hn34qDDvhPRichfT7HDKb+hw0UVZ26GkyRnDztZ67EzmE=; _gid=GA1.2.948675952.1629894104; _dc_gtm_UA-40723232-1=1; _gat_UA-40723232-1=1; __cq_seg=0~0.10!1~-0.26!2~-0.28!3~-0.13!4~0.25!5~-0.25!6~-0.65!7~0.33!8~-0.06!9~-0.41!f0~31~25!n0~1; cto_bundle=1xV6sV9rcm9kVzJnV1JJeVQxM3BhY0c1QXViSU43Y2g1aTdMVXI4ZE1oNzlaZU9pZWcyV0VncUV3WSUyQmppQWo0eEdUbWllYVVpMFdtR3FMdEZpdzVLcXM0eXdWTWJ5RFZSWmFINlVpcE90alJBRkklMkZQZnVKNzVra2JsTDRzcDV0YmRjV3Z6YkRDRTBrcmZJUDlzOHN1UE5YUCUyQkElM0QlM0Q',
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://www.slamjam.com/en_IT/home",
        "sec - ch - ua": '"Chromium";v = "92", " Not A;Brand";v = "99", "Google Chrome";v = "92"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    }

    def start_requests(self):
        url1 = 'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_IT/Search-UpdateGrid?cgid=W100SNE&start=0&sz=100000'
        yield scrapy.Request(url=url1, meta={'gender': 'Female'}, headers=self.headers)
        url2 = 'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_IT/Search-UpdateGrid?cgid=WW100SNE&start=0&sz=100000'
        yield scrapy.Request(url=url2, meta={'gender': 'Male'}, headers=self.headers)

    def parse(self, response, **kwargs):
        for res in response.css('div[itemprop="itemListElement"]'):
            link = res.css('.product-tile a::attr(href)').extract_first()
            if 'javascript:void(0)' in link:
                continue
            url = 'https://www.slamjam.com' + link
            yield scrapy.Request(url=url, callback=self.parse_data, meta={'gender': response.meta['gender']}, headers=self.headers)

    def parse_data(self, response):
        item = dict()
        item['brand'] = response.css('.product-sidebar-inner h2.t-up::text').extract_first()
        item['name_en'] = response.css('.product-sidebar-inner h1.product-name::text').extract_first()
        item['gender'] = response.meta['gender']
        JS = response.css('script[type="application/ld+json"] ::text').extract()[-1].strip()
        JD = json.loads(JS)
        for rs in response.css('.variants.my-3 .variant'):
            if rs.css('.color-value.swatch-circle.swatch-value.selectable.selected'):
                item['color'] = rs.css('.text-lowercase.overflow-hidden::text').extract_first('not available')
            # item['size'] = res.css('::text').extract_first()
        item['group_sku'] = JD['contentUrl'].split('/')[-1].split('.')[0]
        item['product_sku'] = item['group_sku']
        item['description_en'] = JD['description']
        item['main_category'] = response.css('.breadcrumb-item a span::text').extract()[1]
        item['category'] = response.css('.breadcrumb-item a span::text').extract()[2]
        item['sub_category'] = response.css('.breadcrumb-item a span::text').extract()[3]
        item['base_category'] = '/'.join(response.css('.breadcrumb-item a span::text').extract())
        item['material'] = ', '.join(response.css('.descr.descr--long li::text').extract()[:-1])
        item['origin'] = "website"
        # item['size_slug'] = item['size']
        item['description_plain_en'] = JD['description']
        item['delivery_information'] = ' '.join(' '.join(response.css('.accordion-details  div:nth-child(6) p:nth-child(2)::text').extract()).split('(for countries included in  )'))
        # item['variation_type'] = item['size']+' - '+item['color']
        item['serial_no'] = response.css('.product-id::text').extract_first()
        try:
            item['strike_through_price'] = response.css('.strike-through.list .value::text').extract_first().replace('€', '').replace(',', '.').strip()
        except:
            pass
        item['original_price'] = float(response.css('.price .sales .value::attr(content)').extract_first())
        item['whole_sale_price'] = float(response.css('.price .sales .value::attr(content)').extract_first())
        item['retail_price'] = float(response.css('.price .sales .value::attr(content)').extract_first())
        item['main_pic'] = 'https://www.slamjam.com' + response.css('.gallery__wrap img')[0].css('img::attr(data-src)').extract_first()
        for i, img in enumerate(response.css('.gallery__wrap img')):
            if i > 36:
                continue
            item[f'image_{i + 1}'] = 'https://www.slamjam.com' + img.css('img::attr(data-src)').extract_first()
        index = 0
        for res in response.css('#select-prenotation option')[1:]:
            if res.css('option[disabled]'):
                continue
            index += 1
            item['variant_{}'.format(index)] = res.css('::text').extract_first()
            item['variant_{}_price'.format(index)] = float(response.css('.price .sales .value::attr(content)').extract_first())

            #     processed.append(item)
            #     j+=1
            # if len(processed) > 2:
            #     odooClient.insert_records(processed,vendor)
            #     processed.clear()
            writer.writerow(item)
            fileout.flush()

    # def close(spider, reason):
    #     if len(processed) > 1:
    #         odooClient.insert_records(processed,vendor)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(slamjam)
process.start()
