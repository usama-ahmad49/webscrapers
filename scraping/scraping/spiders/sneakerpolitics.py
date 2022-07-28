import csv
import json
import time

import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

gender = ["mens", "women", "children"]
# colnames = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
#             'name_en', "original_price", 'retail_price', 'whole_sale_price', 'description_en', 'main_pic', 'pic1', 'pic2', 'pic3', 'pic4', 'pic5', 'gender',
#             'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
#             'description_plain_en', 'delivery_information', 'badges_en', 'additional_categories', 'restrict_payment', 'meta_title_en',
#             'meta_keyword_en', 'meta_description_en', 'status', 'operation', 'state', 'image_thumbnails', 'search_terms', 'website_ids',
#             'product_tmpl_id', 'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_date_deadline', 'activity_summary',
#             'activity_exception_decoration', 'activity_exception_icon', 'message_is_follower', 'message_follower_ids', 'message_partner_ids',
#             'message_channel_ids', 'message_ids', 'message_unread', 'message_unread_counter', 'message_needaction', 'message_needaction_counter',
#             'message_has_error', 'message_has_error_counter', 'message_main_attachment_id', 'website_message_ids', 'message_has_sms_error',
#             'message_attachment_count', 'id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date', '__last_update']
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

csvfile = open('sneakerpolitics.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


class SneakerPolitics(scrapy.Spider):
    name = "sneakerpolitics"
    break_empty = True
    page = 0

    def start_requests(self):
        for genders in gender:
            yield scrapy.Request(url="https://sneakerpolitics.com/collections/{}/sneakers".format(genders),
                                 meta={"gender": genders})

    def parse(self, response, **kwargs):
        page_number = 1
        while page_number < 50:
            yield scrapy.Request(url=response.url + f'?page={page_number}', callback=self.parsedata, meta={'gender': response.meta['gender']})
            print(response.url + f'?page={page_number}')
            page_number += 1
    def parsedata(self, response, **kwargs):

        resp = scrapy.Selector(text=response.text)

        for total_products in resp.css(
                "div.collection-product-cards div.collection-product-card a.product-card__link::attr(href)").getall():
            title = total_products.rsplit("/", 1)[1]
            yield scrapy.Request(
                url="https://sneakerpolitics.com/collections/{}/products/{}.js".format(response.meta["gender"], title),
                callback=self.scrape_data, meta={"urlkey": title})

    def scrape_data(self, response):
        # g = 4
        resp = json.loads(response.text)
        item = dict()
        item["serial_no"] = resp["id"]
        item["group_sku"] = resp['variants'][0]['sku'].split('|')[0]
        item["product_sku"] = resp['variants'][0]['sku'].split('|')[0]
        # item["urlkey"] = response.meta["urlkey"]
        item["name_en"] = resp["title"]
        item["brand"] = resp["vendor"]
        item["product_type"] = resp["type"]
        item["original_price"] = float(resp["price"] / 100)
        item["retail_price"] = float(resp["price"] / 100)
        item["whole_sale_price"] = float(resp["price"] / 100)
        item["strike_through_price"] = float(resp["compare_at_price_max"] / 100)
        item["gender"] = resp["tags"][1]
        item["main_category"] = resp["tags"][2]
        item["category"] = resp["tags"][3]
        item["base_category"] = item["main_category"] + '/' + item["category"]
        item["origin"] = "website"
        item["size_slug"] = ', '.join(resp["options"][0]['values'])
        item["size"] = ', '.join(resp["options"][0]['values'])

        res = scrapy.Selector(text=resp["description"])
        for k in [v for v in res.css('::text').extract() if '\n' not in v]:
            if 'Style' in k:
                item['StyleId'] = k.split(':')[-1].strip()
            elif 'Color' in k:
                item['color'] = k.split(':')[-1].strip()

        item["description_en"] = ' '.join([v for v in res.css('::text').extract() if '\n' not in v])
        item["description_plain_en"] = ' '.join([v for v in res.css('::text').extract() if '\n' not in v])

        for counter, key in enumerate(resp["variants"]):
            try:
                item['variant_{}'.format(counter + 1)] = key['sku']
            except:
                item['variant_{}'.format(counter + 1)] = 'oneSize'
            try:
                item['variant_{}_price'.format(counter + 1)] = float(key['price'] / 100)
            except:
                item['variant_{}_price'.format(counter + 1)] = 0.0
        item['main_pic'] = resp["images"][0]
        for cntr, image in enumerate(resp["images"]):
            if cntr > 36:
                break
            item[f'pic_{cntr + 1}'] = image
        writer.writerow(item)
        csvfile.flush()
        # try:
        #     item["description"] = re.findall("<p[^>]*>(.*?)</p>",resp["description"])[0].replace("<br>","").replace("</br>","")
        # except:
        #     item["description"] = re.findall("<span[^>]*>(.*?)</span>",resp["description"])[0].replace("<span>","")
        # g = 5


process = CrawlerProcess({})
process.crawl(SneakerPolitics)
process.start()
