import random
import scrapy
import requests
import json
import csv
from scrapy.crawler import CrawlerProcess
# import odooApi
# from currency_converter import CurrencyConverter
# c = CurrencyConverter()

# processed = []
# odooClient = odooApi.odooClient()
vendor = 'kickz'
currency = 'EUR'

headers_csv = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "strike_through_price","original_price", 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
               'description_plain_en', 'delivery_information','main_pic',

               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9","pic_10", "pic_11", "pic_12", "pic_13", "pic_14",
               "pic_15", "pic_16", "pic_17","pic_18", "pic_19", "pic_20", "pic_21", "pic_22", "pic_23", "pic_24", "pic_25","pic_26", "pic_27",
               "pic_28", "pic_29", "pic_30", "pic_31", "pic_32", "pic_33","pic_34", "pic_35", "pic_36",

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
colnames = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
            'name_en','strike_through_price', "original_price",'retail_price', 'whole_sale_price', 'description_en', 'main_pic', 'pic1', 'pic2', 'pic3', 'pic4', 'pic5', 'gender',
            'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
            'description_plain_en', 'delivery_information', 'badges_en', 'additional_categories', 'restrict_payment', 'meta_title_en',
            'meta_keyword_en', 'meta_description_en', 'status', 'operation', 'state', 'image_thumbnails', 'search_terms', 'website_ids',
            'product_tmpl_id', 'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_date_deadline', 'activity_summary',
            'activity_exception_decoration', 'activity_exception_icon', 'message_is_follower', 'message_follower_ids','message_partner_ids',
            'message_channel_ids', 'message_ids', 'message_unread', 'message_unread_counter', 'message_needaction', 'message_needaction_counter',
            'message_has_error', 'message_has_error_counter', 'message_main_attachment_id', 'website_message_ids', 'message_has_sms_error',
            'message_attachment_count', 'id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date', '__last_update']

fileout = open('kickz.csv', mode='w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()

class kickz(scrapy.Spider):
    name = 'kickz'
    # custom_settings = {
    #     'AUTOTHROTTLE_ENABLED': True,
    #     'ROBOTSTXT_OBEY': False,
    #     'DOWNLOAD_TIMEOUT': 1000,
    #     # 'HTTPCACHE_ENABLED' : True,
    #     # 'CONCURRENT_REQUESTS': 1,
    #     'RETRY_TIMES': 5,
    #     'RETRY_HTTP_CODES': [302, 503],
    #     'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
    #     'CRAWLERA_ENABLED': True,
    #     'CRAWLERA_APIKEY': '2d28dd59b4034a60987c38523624a091',
    # }
    start_urls = ['https://www.kickz.com/de/l/schuhe/m%C3%A4nner/sneaker/', 'https://www.kickz.com/de/l/schuhe/frauen/sneaker/', 'https://www.kickz.com/de/l/schuhe/kinder/sneaker-toddler/']
    start = 0
    sz = 50
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'dwanonymous_16eafe6820142d7a9a24d5364ce6a486=bdgCTzALxMCZmTLbqYa8Lqtzw5; __cq_dnt=1; dw_dnt=1; _gcl_au=1.1.388149389.1627560321; mvc=1vjpdvgsh.1627560321498; _ga=GA1.2.611821167.1627560324; sid=kOsj_v_zcMYtKeK5Nvfa3W4B2-HfqeQiuME; appliedPricebooksLocale=de_DE; dwsid=jzPRz4anpHarvjTxl54E2nHZKdCm_TCSPlZjq35lhv9KwoIzxlwPN8NDLYMttthlrriR511Jx_BKzSIKEN7N1Q==; _abck=4E2D9412D23541C4F9E36C0580F100CC~0~YAAQhWvcFwJv8bB6AQAAvrfSBgZ8aHliNB5Lxe5vwWYy6tMUZN9vDsHwzDd5VePkkC+J4O5zSOhUbv1xxULQv6emsa/Io/hTo78QKa5EhECAn5ek/6VDOOgcY2cZr25LK6O35FATKniSiHBiUmSP62ot4+i9Ze/l3GdhTFUHof1gjRYFf7ZFDKes+QQmBDVi3ZuURNNwDF63/ckq1IQaByYxgigfrXorSNwkul9io01elwx6mWV1nj277RxIn0M07C0zcvKcXTXZ1HXvCLUTihxLnMsx1HIHhCQ/3o2Ll93rg4xRatJHE4siAzaPnijeynm+eotzg7TFCXTB7FqPSlxK9S6BVWDEWVaJcdYO5OsgNfduihT/eUMfZO1ueKp6CLMrEp4USm1e6nEYQnt25CG3D1W0X5Q=~-1~-1~-1; bm_sz=E897B4D0DE07FE3406D14E2F6600F7DC~YAAQhWvcFwRv8bB6AQAAvrfSBgyjNRCxykYiP97DBwRAgfdQIOcuOG/vqNbvMEybvrjuXC8gmgcaVRuozSun9ny1nb1ZgQkE2hDZ0Ocdp254YOOwGvzU7jvxRlBaRgh5fNQz1frZAtwiqpOK+yvWGyfgWUHtFAt6M5jPDMgZZOOSGXEWf6o1E8OQdrf6q+WHQL1nM4iIaGQLZNcAmel4MbThTK/0eDUyURh9B17PTEvgK+PPoAPqzccuYI1M1vN22+EnTBseE/6DWPJCLyCZg9BmzBQqowUAteQ1tgnMSHSaQA==~3617092~4536121; _gid=GA1.2.696198970.1627907080; RT="z=1&dm=kickz.com&si=0d454a81-fb63-4c60-8d34-4eab87ce68ff&ss=kruqud5m&sl=3&tt=2kn&bcn=%2F%2F6852bd0a.akstat.io%2F&ld=39cq"',
        'referer': 'https://www.kickz.com/de/p/jordan-sneaker-air-jordan-1-low-black-particle-grey-white/no-referrer',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    def parse(self, response, **kwargs):
        total_items = response.css('.b-load_progress-description::text')[0].extract().split(' ')[2]
        while(self.start <= int(total_items.replace('.', ''))+50):
            yield scrapy.Request(url=f'https://www.kickz.com/de/l/schuhe/?start={self.start}&sz={self.sz}', callback=self.scrape_product_links, )
            self.start += self.sz

    def scrape_product_links(self, response):
        for link in response.css('.b-product_tile .b-product_tile-top a[data-tau="product_image"]::attr(href)').extract():
            yield scrapy.Request(url=f'https://www.kickz.com{link}', callback=self.scrape_data_link, )


    def scrape_data_link(self, response):
        jsstring= response.css('script[type="application/ld+json"] ::text').extract_first().strip()
        jData = json.loads(jsstring)
        item = dict()
        item['name_en'] = jData['name']
        item['brand'] = jData['brand']['name']
        item['group_sku'] = response.css('.b-product_details-manufacturer::text').extract_first().strip()
        # item['product_sku'] = ''
        item['product_sku'] = response.css('.b-product_details-manufacturer::text').extract_first().strip()
        # currencyAvailible = jData['offers']['priceCurrency']
        # eurPrice = float(jData['offers']['price'])
        item['original_price'] = float(jData['offers']['price'])
        # USDPrice = c.convert(eurPrice, currencyAvailible, 'USD')
        try:
            item['strike_through_price'] = response.css('span[data-tau-price="old"]::text').extract_first().strip().replace(',','.').replace(' €','')
        except:
            pass
        item['serial_no'] = jData['mpn']
        item['whole_sale_price'] = float(jData['offers']['price'])
        item['retail_price'] = float(jData['offers']['price'])
        # if j == 0:
        #     item['serial_no'] = jData['mpn']+'AED'
        #     item['whole_sale_price'] = (50 + ((USDPrice) * 1.13)) * 4.86
        #     item['retail_price'] = (50 + ((USDPrice) * 1.13)) * 4.86
        # if j == 1:
        #     item['serial_no'] = jData['mpn']+'KSA'
        #     item['whole_sale_price'] = ((((50 + ((USDPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((USDPrice) * 1.13)) * 4.86
        #     item['retail_price'] = ((((50 + ((USDPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((USDPrice) * 1.13)) * 4.86
        item['description_en'] = ''.join(response.css('#product-details-1 ::text').extract()).strip()
        item['gender'] = response.css('ul.b-breadcrumbs-list li')[2].css('a.b-breadcrumbs-link::text').extract_first().strip()
        item['main_category'] = response.css('ul.b-breadcrumbs-list li')[1].css('a.b-breadcrumbs-link::text').extract_first().strip()
        item['category'] = response.css('ul.b-breadcrumbs-list li')[3].css('a.b-breadcrumbs-link::text').extract_first().strip()
        jsonstring = response.css('.l-pdp-main::attr(data-analytics)').extract_first()
        JD = json.loads(jsonstring)
        item['sub_category'] = JD['category']
        item['base_category'] = ''.join(response.css('ul.b-breadcrumbs-list li a.b-breadcrumbs-link::text').extract()[1:-1]).strip().replace('\n\n', '/')

        # item['size'] = 'multi'
        item['color'] = JD['variant']
        try:
            item['material'] = response.css('#product-details-1 .b-pdp_user_content::text').extract_first().strip()
        except:
            pass
        item['origin'] = "website"
        # item['size_slug'] = 'multi'
        item['description_plain_en'] = ''.join(response.css('#product-details-1 ::text').extract()).strip().replace('\n',' ')
        item['delivery_information'] = ''.join(response.css('div.b-product_details-tax_msg ::text').extract_first().strip().split('.')[2:])

        item['main_pic'] = jData['image'][0]
        for i,img in enumerate(jData['image']):
            if i>36:
                break
            item[f'pic_{i+1}'] = img.split('?')[0]
        # item['variation_type'] = item['size'] +' - '+ item['color']
        index = 0
        for res in response.css('div[aria-label="Größe"] button'):
            if not res.css('.m-disabled'):
                index+=1
                item['variant_{}'.format(index)] =res.css('::attr(title)').extract_first()
                item['variant_{}_price'.format(index)] = float(jData['offers']['price'])
        # processed.append(item)
        writer.writerow(item)
        fileout.flush()
    #             if len(processed) > 200:
    #                 odooClient.insert_records(processed,vendor)
    #                 processed.clear()
    #
    # def close(spider, reason):
    #     if len(processed) > 1:
    #         odooClient.insert_records(processed,vendor)


process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
process.crawl(kickz)
process.start()