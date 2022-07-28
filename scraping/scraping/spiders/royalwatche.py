import csv
import datetime
import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

headers_csv = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
                'name_en', "original_price", 'strike_through_price', 'retail_price', 'whole_sale_price', 'description_en', 'gender',
                'main_category', 'category', 'sub_category', 'base_category', 'size', 'condition','quantity', 'color', 'material', 'origin', 'size_slug',
                'description_plain_en', 'delivery_information', 'main_pic', 'pic_1', 'pic_2', 'pic_3', 'pic_4', 'pic_5', 'pic_6', 'pic_7', 'pic_8', 'pic_9', 'pic_10', 'pic_11', 'pic_12', 'pic_13', 'pic_14',
                'pic_15', 'pic_16', 'pic_17', 'pic_18', 'pic_19', 'pic_20', 'pic_21', 'pic_22', 'pic_23', 'pic_24', 'pic_25', 'pic_26', 'pic_27',
                'pic_28', 'pic_29', 'pic_30', 'pic_31', 'pic_32', 'pic_33', 'pic_34', 'pic_35', 'pic_36',
                "variant_1", "variant_1_stock", "variant_1_price",
                "variant_2", "variant_2_stock", "variant_2_price",
                "variant_3", "variant_3_stock", "variant_3_price",
                "variant_4", "variant_4_stock", "variant_4_price",
                "variant_5", "variant_5_stock", "variant_5_price",
                "variant_6", "variant_6_stock", "variant_6_price",
                "variant_7", "variant_7_stock", "variant_7_price",
                "variant_8", "variant_8_stock", "variant_8_price",
                "variant_9", "variant_9_stock", "variant_9_price",
                "variant_10", "variant_10_stock", "variant_10_price",
                "variant_11", "variant_11_stock", "variant_11_price",
                "variant_12", "variant_12_stock", "variant_12_price",
                "variant_13", "variant_13_stock", "variant_13_price",
                "variant_14", "variant_14_stock", "variant_14_price",
                "variant_15", "variant_15_stock", "variant_15_price",
                "variant_16", "variant_16_stock", "variant_16_price",
                "variant_17", "variant_17_stock", "variant_17_price",
                "variant_18", "variant_18_stock", "variant_18_price",
                "variant_19", "variant_19_stock", "variant_19_price",
                "variant_20", "variant_20_stock", "variant_20_price",
                "variant_21", "variant_21_stock", "variant_21_price",
                "variant_22", "variant_22_stock", "variant_22_price",
                "variant_23", "variant_23_stock", "variant_23_price",
                "variant_24", "variant_24_stock", "variant_24_price",
                "variant_25", "variant_25_stock", "variant_25_price",
                "variant_26", "variant_26_stock", "variant_26_price",
                "variant_27", "variant_27_stock", "variant_27_price",
                "variant_28", "variant_28_stock", "variant_28_price",
                "variant_29", "variant_29_stock", "variant_29_price",
                "variant_30", "variant_30_stock", "variant_30_price",
                "variant_31", "variant_31_stock", "variant_31_price",
                "variant_32", "variant_32_stock", "variant_32_price",
                "variant_33", "variant_33_stock", "variant_33_price",
                "variant_34", "variant_34_stock", "variant_34_price",
                "variant_35", "variant_35_stock", "variant_35_price",
                "variant_36", "variant_36_stock", "variant_36_price",
                "variant_37", "variant_37_stock", "variant_37_price",
                "variant_38", "variant_38_stock", "variant_38_price",
                "variant_39", "variant_39_stock", "variant_39_price",
                "variant_40", "variant_40_stock", "variant_40_price",
                "variant_41", "variant_41_stock", "variant_41_price",
                "variant_42", "variant_42_stock", "variant_42_price",
                "variant_43", "variant_43_stock", "variant_43_price",
                "variant_44", "variant_44_stock", "variant_44_price",
                "variant_45", "variant_45_stock", "variant_45_price",
                "variant_46", "variant_46_stock", "variant_46_price",
                "variant_47", "variant_47_stock", "variant_47_price",
                "variant_48", "variant_48_stock", "variant_48_price",
                "variant_49", "variant_49_stock", "variant_49_price",
                "variant_50", "variant_50_stock", "variant_50_price",
                "variant_51", "variant_51_stock", "variant_51_price",
                "variant_52", "variant_52_stock", "variant_52_price",
                "variant_53", "variant_53_stock", "variant_53_price",
                "variant_54", "variant_54_stock", "variant_54_price",
                "variant_55", "variant_55_stock", "variant_55_price",
                "variant_56", "variant_56_stock", "variant_56_price",
                "variant_57", "variant_57_stock", "variant_57_price",
                "variant_58", "variant_58_stock", "variant_58_price",
                "variant_59", "variant_59_stock", "variant_59_price",
                "variant_60", "variant_60_stock", "variant_60_price",
                "variant_61", "variant_61_stock", "variant_61_price",
                "variant_62", "variant_62_stock", "variant_62_price",
                "variant_63", "variant_63_stock", "variant_63_price",
                "variant_64", "variant_64_stock", "variant_64_price",
                "variant_65", "variant_65_stock", "variant_65_price",
                "variant_66", "variant_66_stock", "variant_66_price",
                "variant_67", "variant_67_stock", "variant_67_price",
                "variant_68", "variant_68_stock", "variant_68_price",
                "variant_69", "variant_69_stock", "variant_69_price",
                "variant_70", "variant_70_stock", "variant_70_price",
                "variant_71", "variant_71_stock", "variant_71_price",
                "variant_72", "variant_72_stock", "variant_72_price",
                "variant_73", "variant_73_stock", "variant_73_price",
                "variant_74", "variant_74_stock", "variant_74_price",
                "variant_75", "variant_75_stock", "variant_75_price",
                "variant_76", "variant_76_stock", "variant_76_price",
                "variant_77", "variant_77_stock", "variant_77_price",
                "variant_78", "variant_78_stock", "variant_78_price",
                "variant_79", "variant_79_stock", "variant_79_price",
                "variant_80", "variant_80_stock", "variant_80_price",
                "variant_81", "variant_81_stock", "variant_81_price",
                "variant_82", "variant_82_stock", "variant_82_price",
                "variant_83", "variant_83_stock", "variant_83_price",
                "variant_84", "variant_84_stock", "variant_84_price",
                "variant_85", "variant_85_stock", "variant_85_price",
                "variant_86", "variant_86_stock", "variant_86_price",
                "variant_87", "variant_87_stock", "variant_87_price",
                "variant_88", "variant_88_stock", "variant_88_price",
                "variant_89", "variant_89_stock", "variant_89_price",
                "variant_90", "variant_90_stock", "variant_90_price",
                "variant_91", "variant_91_stock", "variant_91_price",
                "variant_92", "variant_92_stock", "variant_92_price",
                "variant_93", "variant_93_stock", "variant_93_price",
                "variant_94", "variant_94_stock", "variant_94_price",
                "variant_95", "variant_95_stock", "variant_95_price",
                "variant_96", "variant_96_stock", "variant_96_price",
                "variant_97", "variant_97_stock", "variant_97_price",
                "variant_98", "variant_98_stock", "variant_98_price",
                "variant_99", "variant_99_stock", "variant_99_price",
                "variant_100", "variant_100_stock", "variant_100_price"
                ]
fileout = open('royalwatche.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')


class royalwatche(scrapy.Spider):
    name = 'royalwatche'

    def start_requests(self):
        '''mens watches'''
        resmw = requests.get('https://royalwatche.com/product-category/watches/')
        respmw = scrapy.Selector(text=resmw.text)
        TotalPagesmw = int(respmw.css('ul.page-numbers li')[-2].css('a::text').extract_first())
        mw = 1
        while mw <= TotalPagesmw:
            linkmw = f'https://royalwatche.com/product-category/watches/page/{mw}/'
            yield scrapy.Request(url=linkmw, meta={'maincategory': 'Men', 'category': 'watches'})
            mw += 1

        '''women watches'''
        resww = requests.get('https://royalwatche.com/product-category/womens-watches/')
        respww = scrapy.Selector(text=resww.text)
        TotalPagesww = int(respww.css('ul.page-numbers li')[-2].css('a::text').extract_first())
        ww = 1
        while ww <= TotalPagesww:
            linkww = f'https://royalwatche.com/product-category/womens-watches/page/{ww}/'
            yield scrapy.Request(url=linkww, meta={'maincategory': 'Women', 'category': 'watches'})
            ww += 1

    def parse(self, response, **kwargs):
        for res in response.css('.products a.woocommerce-LoopProduct-link.woocommerce-loop-product__link'):
            urlprod = res.css('::attr(href)').extract_first()
            yield scrapy.Request(url=urlprod, callback=self.parse_prod, meta={'maincategory': response.meta['maincategory'], 'category': response.meta['category']})

    def parse_prod(self, response):
        item = dict()
        jstring = response.css('script[type="application/ld+json"]::text').extract_first()
        data = json.loads(jstring)
        if '@graph' in data.keys():
            item['group_sku'] = str(data['@graph'][1]['sku'])
            item['name_en'] = data['@graph'][1]['name']
            item['original_price'] = data['@graph'][1]['offers'][0]['price']
            item['retail_price'] = data['@graph'][1]['offers'][0]['price']
            item['whole_sale_price'] = data['@graph'][1]['offers'][0]['price']
        else:
            item['name_en'] = response.css('h1::text').extract_first()
            if response.css('.price.retail::text').extract_first() == None:
                item['strike_through_price'] = 'Price on request'
                item['original_price'] = 'Price on request'
                item['retail_price'] = 'Price on request'
                item['whole_sale_price'] = 'Price on request'
            else:
                item['strike_through_price'] = response.css('.price.cross::text').extract_first().strip()
                item['original_price'] = response.css('.price.retail::text').extract_first()
                item['retail_price'] = response.css('.price.retail::text').extract_first()
                item['whole_sale_price'] = response.css('.price.retail::text').extract_first()

        i = 0
        while i < len(response.css('#specification ul li')):
            if response.css('#specification ul li')[i + 1].css('::text').extract_first() == None:
                i += 2
                continue
            if 'Ref No.' in response.css('#specification ul li')[i].css('::text').extract_first():
                if 'group_sku' not in item.keys():
                    item['group_sku'] = response.css('#specification ul li')[i + 1].css('::text').extract_first()
                    i += 2
                    continue
            if 'Brand' in response.css('#specification ul li')[i].css('::text').extract_first():
                item['brand'] = response.css('#specification ul li')[i + 1].css('::text').extract_first()
                i += 2
                continue

            if 'Case material' in response.css('#specification ul li')[i].css('::text').extract_first():
                item['material'] = response.css('#specification ul li')[i + 1].css('::text').extract_first()
                i += 2
                continue
            if 'Bracelet Material' in response.css('#specification ul li')[i].css('::text').extract_first():
                item['material'] = item['material'] + ' - ' + response.css('#specification ul li')[i + 1].css('::text').extract_first()
                i += 2
                continue

            if 'Condition' in response.css('#specification ul li')[i].css('::text').extract_first():
                item['condition'] = response.css('#specification ul li')[i + 1].css('::text').extract_first()
                i += 2
                continue

            if 'Gender' in response.css('#specification ul li')[i].css('::text').extract_first():
                item['gender'] = response.css('#specification ul li')[i + 1].css('::text').extract_first()
                i += 2
                continue
            i += 2
        item['ref'] = TS
        # item['product_type'] = data['type']
        # item['group_sku'] = data['dimension4']

        item['description_en'] = '\n'.join(response.css('.woocommerce-product-details__short-description ::text').extract())
        item['main_category'] = response.meta['maincategory']
        item['category'] = response.meta['category']
        item['sub_category'] = item['name_en']
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        # item['color'] = data['colour']
        item['origin'] = 'website'
        # try:
        #     item['size_slug'] = [re.findall(r'(\w+?)(\d+)', data['availableSizes'][0])[0]][0][0]
        # except:
        #     item['size_slug'] = data['availableSizes'][0]
        item['description_plain_en'] = '\n'.join(response.css('.woocommerce-product-details__short-description ::text').extract())
        item['delivery_information'] = '15 to 20 days'
        item['main_pic'] = response.css('.woocommerce-product-gallery__image a::attr(href)').extract_first()
        item[f'pic_1'] = response.css('.woocommerce-product-gallery__image a::attr(href)').extract_first()
        item[f'variant_1'] = item['group_sku']
        try:
            if 'InStock' in data['@graph'][1]['offers'][0]['availability']:
                item[f'variant_1_stock'] ='In Stock'
        except:
            item[f'variant_1_stock'] = 'Out of Stock'
        item[f'variant_1_price'] =item['original_price']
        item['group_sku'] = response.url
        # for i, res in enumerate(response.css('.p-images__preview-swatches img')):
        #     if i > 36:
        #         break
        #     item[f'pic_{i + 1}'] = res.css('::attr(src)').extract_first().split('?')[0]
        # index = 0
        # for sz in data['availableSizes']:
        #     try:
        #         item[f'variant_{index + 1}'] = [re.findall(r'(\w+?)(\d+)', sz)[0]][0][1]
        #     except:
        #         item[f'variant_{index + 1}'] = sz
        #     item[f'variant_{index + 1}_price'] = str(data['price']) + ' ' + dataB['ecommerce']['currencyCode']
        #     index += 1
        writer.writerow(item)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(royalwatche)
process.start()
