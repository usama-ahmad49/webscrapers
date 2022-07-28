import csv
import datetime
import json
import os
import time

import csvdiff
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

cwd = os.getcwd()

# '''file for magento'''
# priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
# pricemagentostockx = open('stockx_pricelist_magento_old_temp.csv', 'w', newline='', encoding='utf-8')
# pricewriterstockx = csv.DictWriter(pricemagentostockx, fieldnames=priceupdateheaders)
# pricewriterstockx.writeheader()
#
# '''file for pricelist'''
# pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
# pricelistfilestockx = open('stockx_pricelist_odoo_old_temp.csv', 'w', newline='', encoding='utf-8')
# pricelistwriterstockx = csv.DictWriter(pricelistfilestockx, fieldnames=pricelistheaders)
# pricelistwriterstockx.writeheader()

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')

fileoutput = open('reverseStockx.txt', 'r')
links = fileoutput.read().split('\n')
links = [p for p in links if p]

headers_csv = ['serial_no', 'ref', 'url_key', 'partner_id', 'product_type', 'is_image_360', 'group_sku', 'condition', 'ticker', 'StyleId',
               'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "original_price", 'retail_price', 'whole_sale_price', 'description_en', 'gender',
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


def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class StockX(scrapy.Spider):
    name = "stock_x"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'stockx_experiments_id=web-410547fe-366d-4695-9c14-ec7bb493c03a; language_code=en; stockx_market_country=PK; _ga=GA1.2.788108403.1627381998; pxcts=0e9c4630-eec6-11eb-8f35-456c805b484e; _pxvid=0e9c0b7f-eec6-11eb-bd74-0242ac120005; _gcl_au=1.1.157424790.1627381999; _scid=d66f0315-e66c-43f7-9088-cb913be1d684; _fbp=fb.1.1627381999323.1551633080; below_retail_type=; product_page_affirm_callout_enabled_web=false; riskified_recover_updated_verbiage=true; home_vertical_rows_web=true; ops_banner_id=blteaa2251163e21ba6; _px_f394gi7Fvmc43dfg_user_id=MTA0OTU5ZjEtZWVjNi0xMWViLTkzMWQtNzU0NDc2NWQ2YjUy; QuantumMetricUserID=d09c7fd3ca35f4883252442e93c26ffb; rskxRunCookie=0; rCookie=o5z2ngw5qrkce8yubt0e7tkrlx854q; __pdst=889c3ece03e34c9b91f9e7bf94bb5d0f; IR_gbd=stockx.com; _rdt_uuid=1627382004357.08170ccd-84e5-4727-b809-30b9e8d7868b; __ssid=3ff3af1fd98b9b60409658d135799ec; __pxvid=87150fcf-0428-11ec-a4f3-0242ac110002; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2021-08-23T15%3A41%3A08.740Z; stockx_dismiss_modal_expiration=2021-08-30T15%3A41%3A08.739Z; stockx_default_sneakers_size=All; stockx_homepage=sneakers; _ts_yjad=1629827453266; _gid=GA1.2.778798068.1629974367; _pxff_rf=1; _gat=1; stockx_session=TNgOJDcB1xS6iIYqhH1O-; ajs_group_id=ab_android_aa_ramping.neither%2Cab_android_aa_ramping_multi.d1%2Cab_android_home_consolidate_q221.dummy%2Cab_buy_order_status_reskin_android.niether%2Cab_consolidated_home_ios.variant_2%2Cab_enable_eu_vat_collection_ios.true%2Cab_eu_vat_android.true%2Cab_ios_aa_ramping.neither%2Cab_ios_aa_ramping_multi.d1%2Cab_ios_localized_low_inv_checkout_v3.neither%2Cab_low_inventory_expansion_v2_android.neither%2Cab_new_checkout_flow_v2_ios.neither%2Cab_new_restock_pdp_android.true%2Cab_personalized_layout_ios.neither%2Cab_pirate_buy_now_web.true%2Cab_pirate_highlight_searchbar_web.false%2Cab_pirate_payment_reorder_web.true%2Cab_product_page_refactor_android_v5.neither%2Cab_product_page_refactor_web.true%2Cab_product_size_chart_ios.true%2Cab_rage_click_web.false%2Cab_recently_viewed_home_web.true%2Cab_recently_viewed_pdp_ios.neither%2Cab_refactor_selling_payment_android.neither%2Cab_sell_button_color_ios.dummy%2Cab_seller_profile_redesign_android.false%2Cab_suggested_addresses_android.neither%2Cab_test_korean_language_web.true; ajs_anonymous_id=53153b99-1102-46c6-94cc-b72e698153dc; QuantumMetricSessionID=390d23b4306cf7ce5e3f4b4a5a4a954a; _dd_s=rum=0&expire=1629975276829; stockx_product_visits=37; _uetsid=e3db9960065911eca62a6d6bcb897900; _uetvid=0f591ae0eec611eb9ff5fdfee065b825; _px3=f7999bf29f65abc61b4d75152f1812272508a0c4a6e57078c2f80f0a164bce49:hrDVb/Yvf8iR2WFXBbLqkfMZ/4g87jj2CPPHowAwuwkKlPHfET04FfDEHNO5VKANtiYGKlFYwY32Su8q3qsgbQ==:1000:vDbjZunVujAsGnno6gksStGuRaH0/gpI+yz6qJhKblaAPOMqEfO6uMv5ewRZDAykGRIY2iBmTTbqou6QW8tV6y+XZpYZXqdGYbvLJIuUvDYpRP1OkUFEszM2NolQhtfUUtgq24OstUsKxnEy6UC3PYnxBWuamYo2Jfm4IEikn/nQcJvdQ1k/JzTAltrncRa5Dx/OdhbYLHLp/WbulEOsnQ==; forterToken=f97714707aaa44c8bda665516444d4dd_1629974378223__UDF43_13ck; lastRskxRun=1629974379462; IR_9060=1629974381737%7C0%7C1629974381737%7C%7C; IR_PI=124d676f-eec6-11eb-84ad-4f7348310cc7%7C1630060781737; _px_7125205957_cs=eyJpZCI6ImU0ZTM3MjkwLTA2NTktMTFlYy1iMzcwLTg3ZTA4NGI2YWNlMiIsInN0b3JhZ2UiOnt9LCJleHBpcmF0aW9uIjoxNjI5OTc2MTg0MDg5fQ==',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://stockx.com/',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 30,
        'RETRY_HTTP_CODES': [302, 503, 400, 403],
        'Handle_httpstatus_list': [400, 403],
        'ROTATING_PROXY_LIST_PATH': f'{cwd}/proxy.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
        # 'HTTPCACHE_ENABLED': True,
        # 'HTTPCACHE_DIR': 'E:\cache',
        # 'HTTPCACHE_EXPIRATION_SECS': 86400,

    }

    def start_requests(self):
        for urlkey in ['adidas-ultra-boost-20-geometric-black-grey*ADI-ADUB2GBCC']:#links:
            # if urlkey != 'yeezy-slide-desert-sand-infants*YZSLD-DSI-Desert-Sand':
            #     continue
            if urlkey == '':
                continue
            if urlkey == '**this**':
                continue
            # if 'BQ6806-111' in urlkey.split('*')[1]:
            link = 'https://stockx.com/api/products/{}?includes=market,360&currency=USD&country=AE'.format(
                urlkey.split('*')[0])
            yield scrapy.Request(link, callback=self.parse_product, meta={
                'skuold': urlkey.split('*')[1],
                'tries': 0,
                'urlkey': urlkey,
                'link': link
            }, headers=self.headers, dont_filter=True)

    def parse_product(self, response):
        try:
            jdata = json.loads(response.text)
        except:
            yield scrapy.Request(response.meta['link'], callback=self.parse_product, meta={
                'skuold': response.meta['skuold'],
                'tries': response.meta['tries'],
                'urlkey': response.meta['urlkey'],
                'link': response.meta['link']
            }, dont_filter=True, headers=self.headers)
            return
        product = jdata['Product']
        # i = 0
        # while i < 2:
        item = dict()
        item['brand'] = product['brand'].title()
        item['name_en'] = product['title'].title()
        item['gender'] = product['gender'].title()
        item['ticker'] = product['tickerSymbol']
        try:
            item['StyleId'] = product['styleId']
        except:
            try:
                item['StyleId'] = response.meta['datajson']['styleId']
            except:
                item['StyleId'] = ''
        try:
            item['condition'] = product['condition'].title()
        except:
            pass
        # item['variation_type'] = 'Size'
        try:
            color = product['colorway'].split('/')[0].strip().title()
        except:
            color = product['name'].strip().title()

        for clr in color.split():
            if check_color(clr):
                item['color'] = clr
        if 'color' not in item.keys():
            item['color'] = color
        try:
            item['original_price'] = int(product['retailPrice'])
        except:
            try:
                item['original_price'] = int(product['market']['lowestAsk'])
            except:
                item['original_price'] = int(response.meta['datajson']['retailPrice'])
        try:
            # if i == 0:
            item['serial_no'] = product['id'] + 'AED'

            try:
                item['whole_sale_price'] = int((50 + (item['original_price'] * 1.13)) * 4.86)
            except:
                item['whole_sale_price'] = int((50 + (response.meta['datajson']['retailPrice'] * 1.13)) * 4.86)
            try:
                item['retail_price'] = int((50 + (item['original_price'] * 1.13)) * 4.86)
            except:
                item['retail_price'] = int((50 + (response.meta['datajson']['retailPrice'] * 1.13)) * 4.86)

        except:
            pass
        # item['group_sku'] = product['tickerSymbol'] + '-' + item['color']  # response.meta['skuold']
        item['group_sku'] = response.meta['skuold'].replace("'", "")  # product['tickerSymbol'] + '-' + item['color']

        item['url_key'] = product['shortDescription']
        item['description_en'] = product['description'].replace('<br>', '')
        if item['description_en'] == '':
            item['description_en'] = product['shortDescription']
        try:
            item['main_category'] = product['gender']  # 'Men'  # product['productCategory']
            item['category'] = 'Shoes'  # product['productCategory']
            item['sub_category'] = 'Sneakers'  # product['secondaryCategory']
            item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        except:
            pass
        item['size_slug'] = product['sizeLocale'].split()[0].strip().title()
        item['description_plain_en'] = product['description'].replace('<br>', '')
        if item['description_plain_en'] == '':
            item['description_plain_en'] = product['shortDescription']
        item['delivery_information'] = '15 to 20 days'
        if len(product['media']['360']) != 0:
            item['is_image_360'] = True
        else:
            item['is_image_360'] = False
        images = product['media']['360']
        if len(images) == 0:
            images = product['media']['gallery']

        if not images or images[0] == None:
            images = [product['media']['imageUrl']]
        item['main_pic'] = images[0].split('?')[0]
        for index, image in enumerate(images):
            if index > 35:
                continue
            item['pic_{}'.format(index + 1)] = image.split('?')[0]
        index = 0
        for variant in (list(product['children'].values())):
            # if variant['market']['lowestAsk'] == 0:
            #     continue
            if variant['shoeSize'] == '1':
                continue
            if variant['shoeSize'] != '':
                item['variant_{}'.format(index + 1)] = variant['shoeSize']
            else:
                pass
                # for tr in variant['traits']:
                #     if 'Color' in tr['name']:
                #         item['variant_{}'.format(index + 1)] = tr['value']
                #         break
            try:
                item['variant_{}_price'.format(index + 1)] = int(variant['market']['lowestAsk'])

            except:
                item['variant_{}_price'.format(index + 1)] = 0
            if 'AED' in item['serial_no']:
                for i in range(0, 3):
                    PUitem = dict()
                    try:
                        PUitem['sku'] = item['group_sku'] + '-' + item['variant_{}'.format(index + 1)]
                    except:
                        PUitem['sku'] = item['group_sku'] + '-' + 'OS'
                    if i == 0:
                        PUitem['store_view_code'] = 'en'
                        PUitem['price'] = int((50 + (item['variant_{}_price'.format(index + 1)] * 1.13)) * 4.86)
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index + 1)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif i == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(((((50 + (item['variant_{}_price'.format(index + 1)] * 1.13)) * 4.86) * 10) / 100) + (50 + (item['variant_{}_price'.format(index + 1)] * 1.13)) * 4.86)
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index + 1)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif i == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(((50 + (item['variant_{}_price'.format(index + 1)] * 1.13)) * 4.86) / 3.67)
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index + 1)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    # pricewriterstockx.writerow(PUitem)
                    # pricemagentostockx.flush()

                PLitem = dict()
                PLitem['GROUP SKU'] = item['group_sku']
                try:
                    PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + item['variant_{}'.format(index + 1)]
                except:
                    PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + 'OS'
                PLitem['RETAIL PRICE'] = int((50 + (item['variant_{}_price'.format(index + 1)] * 1.13)) * 4.86)
                if item['variant_{}_price'.format(index + 1)] == 0:
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                # pricelistwriterstockx.writerow(PLitem)
                # pricelistfilestockx.flush()
            index += 1


    # def close(spider, reason):
    #     start = time.time()
    #     pricemagentostockx.close()
    #     pricelistfilestockx.close()
    #
    #     patch = csvdiff.diff_files('stockx_pricelist_magento_old_original.csv', 'stockx_pricelist_magento_old_temp.csv',
    #                                ['sku', 'store_view_code'])
    #     '''delta file for magento'''
    #     deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
    #     deltapriceupdate = open('stockx_pricelist_magento_old_delta.csv', 'w', newline='', encoding='utf-8')
    #     deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
    #     deltapricewriter.writeheader()
    #
    #     originalpriceupdate = open('stockx_pricelist_magento_old_original.csv', 'a+', newline='', encoding='utf-8')
    #     originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
    #
    #     for item in patch['added']:
    #         deltapricewriter.writerow(item)
    #         deltapriceupdate.flush()
    #         originalpriceupdatewriter.writerow(item)
    #         originalpriceupdate.flush()
    #
    #     changed = []
    #     for item in patch['changed']:
    #         item_ = dict()
    #         item_['sku'] = item['key'][0]
    #         item_['store_view_code'] = item['key'][1]
    #         try:
    #             if item['fields']['price']['to'] != '0':
    #                 item_['status'] = '1'
    #             else:
    #                 item_['status'] = '2'
    #             item_['price'] = int(float(item['fields']['price']['to']))
    #         except:
    #             item_['status'] = item['fields']['status']['to']
    #             if item_['status'] == '2':
    #                 item_['price'] = '0'
    #
    #         deltapricewriter.writerow(item_)
    #         deltapriceupdate.flush()
    #         changed.append(item_)
    #     original_list = list(csv.DictReader(open('stockx_pricelist_magento_old_original.csv')))
    #     originalpriceupdate = open('stockx_pricelist_magento_old_original.csv', 'w', newline='', encoding='utf-8')
    #     originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
    #     originalpriceupdatewriter.writeheader()
    #     for o_item in original_list:
    #         for c_item in changed:
    #             if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
    #                 o_item['price'] = int(c_item['price'])
    #                 o_item['status'] = c_item['status']
    #         originalpriceupdatewriter.writerow(o_item)
    #         originalpriceupdate.flush()
    #
    #     ####        odoo code         ####
    #
    #     patch_2 = csvdiff.diff_files('stockx_pricelist_odoo_old_original.csv', 'stockx_pricelist_odoo_old_temp.csv',
    #                                  ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
    #     '''delta file for pricelist'''
    #     deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
    #     deltapricelistfile = open('stockx_pricelist_odoo_old_delta.csv', 'w', newline='', encoding='utf-8')
    #     deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
    #     deltapricelistwriter.writeheader()
    #
    #     originalpricelist = open('stockx_pricelist_odoo_old_original.csv', 'a+', newline='', encoding='utf-8')
    #     originalpricelistwriter = csv.DictWriter(originalpricelist, fieldnames=deltapricelistheaders)
    #
    #     for item in patch_2['added']:
    #         deltapricelistwriter.writerow(item)
    #         deltapricelistfile.flush()
    #         originalpricelistwriter.writerow(item)
    #         originalpricelist.flush()
    #
    #     changed = []
    #     for item in patch_2['changed']:
    #         item_ = dict()
    #         item_['GROUP SKU'] = item['key'][0]
    #         item_['PRODUCT SKU'] = item['key'][1]
    #         item_['WEBSITES'] = item['key'][2]
    #         item_['RETAIL PRICE'] = int(float(item['fields']['RETAIL PRICE']['to']))
    #         deltapricelistwriter.writerow(item_)
    #         deltapricelistfile.flush()
    #         changed.append(item_)
    #
    #     original_list = list(csv.DictReader(open('stockx_pricelist_odoo_old_original.csv')))
    #     originalpriceupdate = open('stockx_pricelist_odoo_old_original.csv', 'w', newline='', encoding='utf-8')
    #     originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
    #     originalpriceupdatewriter.writeheader()
    #     for o_item in original_list:
    #         for c_item in changed:
    #             if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
    #                 o_item['RETAIL PRICE'] = int(c_item['RETAIL PRICE'])
    #         originalpriceupdatewriter.writerow(o_item)
    #         originalpriceupdate.flush()
    #
    #     end = time.time()
    #     print(f"Runtime of the program is {end - start}")


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(StockX)
process.start()
