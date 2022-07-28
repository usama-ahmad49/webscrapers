import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

csv_columns = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'condition', 'ticker', 'StyleId',
               'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', 'strike_through_price', "original_price", 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material',
               'origin', 'size_slug',
               'description_plain_en', 'delivery_information', 'main_pic',

               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9", "pic_10", "pic_11",
               "pic_12", "pic_13", "pic_14",
               "pic_15", "pic_16", "pic_17", "pic_18", "pic_19", "pic_20", "pic_21", "pic_22", "pic_23", "pic_24",
               "pic_25", "pic_26", "pic_27",
               "pic_28", "pic_29", "pic_30", "pic_31", "pic_32", "pic_33", "pic_34", "pic_35", "pic_36",

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


class footshop(scrapy.Spider):
    name = 'footshop'

    def start_requests(self):
        categorylistWoMens = ['categories-womens_autumn_shoes', 'categories-basketball_shoes', 'categories-kids_sneakers_and_shoes', 'categories-limited_edition',
                              'categories-low_top_sneakers_and_shoes', 'categories-mens_shoes', 'categories-mens_mid_tops_high_tops',
                              'categories-premium', 'categories-running_shoes', 'categories-skate_shoes', 'categories-spring_shoes_and_sneakers',
                              'categories-summer_shoes_and_slipers', 'categories-summer_shoes_and_slippers', 'categories-winter_shoes_and_boots',
                              'categories-womens_shoes']
        categorylistMens = ['categories-mens_shoes', 'categories-running_shoes', 'categories-autumn_shoes',
                            'categories-basketball_shoes', 'categories-kids_sneakers_and_shoes',
                            'categories-limited_edition', 'categories-low_top_sneakers_and_shoes',
                            'categories-mens_mid_tops_high_tops', 'categories-premium', 'categories-running_shoes',
                            'categories-skate_shoes', 'categories-spring_shoes_and_sneakers',
                            'categories-summer_shoes_and_slipers', 'categories-summer_shoes_and_slippers',
                            'categories-winter_shoes_and_boots', 'categories-womens_shoes']
        for cat in categorylistMens:
            url = f'https://www.footshop.com/en/4600-men-s-sneakers/{cat}'
            res = requests.get(url)
            resp = scrapy.Selector(text=res.content.decode('utf-8'))
            try:
                totalpagessneakers = resp.css('.PaginationLink_link_13OvK a::text').extract()[-1]
            except:
                totalpagessneakers = 1
            i = 1
            while i <= totalpagessneakers:
                link = f'https://www.footshop.com/en/4600-men-s-sneakers/{cat}/page-{i}'
                yield scrapy.Request(url=link, meta={'category': cat, 'gender':'Men'})

        for catwomen in categorylistWoMens:
            url = f'https://www.footshop.com/en/4789-women-s-sneakers/{catwomen}'
            res = requests.get(url)
            resp = scrapy.Selector(text=res.content.decode('utf-8'))
            try:
                totalpageswomensneakers = resp.css('.PaginationLink_link_13OvK a::text').extract()[-1]
            except:
                totalpageswomensneakers = 1
            i = 1
            while i <= totalpageswomensneakers:
                link = f'https://www.footshop.com/en/4789-women-s-sneakers/{catwomen}/page-{i}'
                yield scrapy.Request(url=link, meta={'category': catwomen, 'gender':'Women'})

        urlbag = 'https://www.footshop.com/en/1128-bags-backpacks'
        yield scrapy.Request(url=urlbag, meta={'category': 'bag', 'gender':'unisex'})

    def parse(self, response, **kwargs):
        jstring = response.css('script[type="application/json"][data-hypernova-key="Catalog"]::text').extract_first().split('<!--')[-1].split('-->')[0]
        jdata = json.loads(jstring)
        for data in jdata['data']['state']['products']['items']:
            item = dict()
            item['serial_no'] = data['id']
            item['group_sku'] = data['code']
            item['ticker'] = data['code']
            item['StyleId'] = data['code']
            item['product_sku'] = data['code']+'-'+data['color']+'-'+data['attributes']['variants'][0]['name']
            item['brand'] = data['manufacturer']['name'].capitalize()
            item['name_en'] = data['title'].capitalize()
            try:
                item['strike_through_price'] = float(data['price']['value_without_reduction'])
            except:
                pass
            item['original_price'] = float(data['price']['value'])
            item['retail_price'] = float(data['price']['value'])
            item['whole_sale_price'] = float(data['price']['value'])
            item['description_en'] = data['name']
            item['gender'] = response.meta['gender']
            item['main_category'] = response.meta['gender']
            item['category'] = data['category_name_en']
            item['sub_category'] = response.meta['category']
            item['base_category'] = item['main_category']+'/'+item['category']+'/'+item['sub_category']
            item['size'] = data['attributes']['variants'][0]['name']
            item['color'] = data['color']
            item['size_slug'] = 'size_us'
            for counter, d in enumerate(data['attributes']['variants']):
                item['variant_{}_price'.format(counter + 1)] =float(data['price']['value'])
                item['variant_{}'.format(counter + 1)] =d['name']

            item['main_pic'] = data['image']
            resimg = requests.get(f'https://www.footshop.com/en/api/product/{data["id"]}')
            ress = json.loads(resimg.text)
            for cntr, image in enumerate(ress["images"]["other"]):
                if cntr > 36:
                    break
                item[f'pic_{cntr + 1}'] = image['image']
            item['quantity'] = ress['availability']['quantity']

        # for res in response.css('.Products_product_1JtLQ'):
        #     url = res.css('.Product_inner_1Refv a::attr(href)').extract_first()
        #     yield scrapy.Request(url=url,callback=self.parse_data ,meta={'category':response.meta['category']})
        # url = 'https://www.footshop.com/en/api/products/similar?id=102451&v=1'


process = CrawlerProcess({})
process.crawl(footshop)
process.start()
