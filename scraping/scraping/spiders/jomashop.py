import concurrent.futures
import csv
import re
import time
import datetime
# import xlsxwriter
import requests

# import pandas as pd
#
# workbook = xlsxwriter.Workbook('output.xlsx')
# worksheet = workbook.add_worksheet()
# row = 0
# col = 0


headers = {
    'authority': 'www.jomashop.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'accept': '*/*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'content-type': 'application/json',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
}

headers_csv = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'condition', 'ticker', 'StyleId',
               'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "original_price", 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material',
               'origin', 'size_slug', 'description_plain_en', 'delivery_information', 'main_pic',

               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9", "pic_10", "pic_11",
               "pic_12", "pic_13", "pic_14", "pic_15", "pic_16", "pic_17", "pic_18", "pic_19", "pic_20", "pic_21",
               "pic_22", "pic_23", "pic_24", "pic_25", "pic_26", "pic_27", "pic_28", "pic_29", "pic_30", "pic_31",
               "pic_32", "pic_33", "pic_34", "pic_35", "pic_36",

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
csvfile = open('output.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
writer.writeheader()


def get_category_info(category_url):
    response = requests.get(category_url, headers=headers)

    category_id = re.findall(r'data-model-id="(.*?)"', response.text)[0]
    print(f'Category ID: {category_id}')

    url = f'https://www.jomashop.com/graphql?query=query%20category(%24id%3AString\u0021%2C%24pageSize%3AInt\u0021%2C%24currentPage%3AInt\u0021%2C%24onServer%3ABoolean\u0021%2C%24filter%3AProductAttributeFilterInput\u0021%2C%24sort%3AProductAttributeSortInput)%7BcategoryList(filters%3A%7Bids%3A%7Bin%3A%5B%24id%5D%7D%7D)%7Bid%20description%20takeshape_intro_description%20name%20url_key%20display_mode%20landing_page%20landing_page_identifier%20breadcrumbs%7Bcategory_level%20category_name%20category_url_key%20category_url_path%20__typename%7Dfeatured_filter%20children%7Bid%20level%20name%20path%20url_path%20url_key%20__typename%7Dmeta_title%40include(if%3A%24onServer)meta_keywords%40include(if%3A%24onServer)meta_description%40include(if%3A%24onServer)canonical_url%40include(if%3A%24onServer)filter_map%7Brequest_var%20value_string%20url%20__typename%7D__typename%7Dproducts(pageSize%3A%24pageSize%2CcurrentPage%3A%24currentPage%2Cfilter%3A%24filter%2Csort%3A%24sort)%7Baggregations%7Battribute_code%20count%20label%20options%7Blabel%20value%20count%20swatch_image%20__typename%7D__typename%7Dsort_fields%7Bdefault%20options%7Blabel%20value%20__typename%7D__typename%7Ditems%7B__typename%20id%20name%20msrp%20price_promo_text%20promotext_value%20promotext_type%20promotext_code%20stock_status%20price_range%7Bminimum_price%7Bregular_price%7Bvalue%20currency%20__typename%7Dfinal_price%7Bvalue%20currency%20__typename%7Dprice_promo_text%20msrp_price%7Bvalue%20currency%20__typename%7Ddiscount_on_msrp%7Bamount_off%20percent_off%20__typename%7Dplp_price%7Bwas_price%20now_price%20discount%20promotext_value%20has_coupon%20__typename%7D__typename%7D__typename%7Dbrand_name%20name_wout_brand%20manufacturer%20special_price%20sku%20small_image%7Burl%20sizes%7Bimage_id%20url%20__typename%7D__typename%7Durl_key%20is_preowned%7Dpage_info%7Btotal_pages%20current_page%20__typename%7Dtotal_count%20__typename%7D%7D&operationName=category&variables=%7B%22currentPage%22%3A1%2C%22id%22%3A{category_id}%2C%22idNum%22%3A{category_id}%2C%22onServer%22%3Atrue%2C%22pageSize%22%3A60%2C%22filter%22%3A%7B%22category_id%22%3A%7B%22eq%22%3A%22{category_id}%22%7D%7D%2C%22sort%22%3A%7B%7D%7D'
    response = requests.get(url, headers=headers)
    json_result = response.json()
    total_products = json_result['data']['products']['total_count']
    total_page = json_result['data']['products']['page_info']['total_pages']

    print(f'{total_products} products | {total_page} page')
    return {
        'category_id': category_id,
        'total_page': total_page,
        'category_name': json_result['data']['categoryList'][0]['name']
    }


def crawl_product_for_page(data):
    i = 0
    while i < 5:
        try:
            category_id = data['category_id']
            page = data['page']
            category_name = data['category_name']

            url = f'https://www.jomashop.com/graphql?query=query%20category(%24id%3AString\u0021%2C%24pageSize%3AInt\u0021%2C%24currentPage%3AInt\u0021%2C%24onServer%3ABoolean\u0021%2C%24filter%3AProductAttributeFilterInput\u0021%2C%24sort%3AProductAttributeSortInput)%7BcategoryList(filters%3A%7Bids%3A%7Bin%3A%5B%24id%5D%7D%7D)%7Bid%20description%20takeshape_intro_description%20name%20url_key%20display_mode%20landing_page%20landing_page_identifier%20breadcrumbs%7Bcategory_level%20category_name%20category_url_key%20category_url_path%20__typename%7Dfeatured_filter%20children%7Bid%20level%20name%20path%20url_path%20url_key%20__typename%7Dmeta_title%40include(if%3A%24onServer)meta_keywords%40include(if%3A%24onServer)meta_description%40include(if%3A%24onServer)canonical_url%40include(if%3A%24onServer)filter_map%7Brequest_var%20value_string%20url%20__typename%7D__typename%7Dproducts(pageSize%3A%24pageSize%2CcurrentPage%3A%24currentPage%2Cfilter%3A%24filter%2Csort%3A%24sort)%7Baggregations%7Battribute_code%20count%20label%20options%7Blabel%20value%20count%20swatch_image%20__typename%7D__typename%7Dsort_fields%7Bdefault%20options%7Blabel%20value%20__typename%7D__typename%7Ditems%7B__typename%20id%20name%20msrp%20price_promo_text%20promotext_value%20promotext_type%20promotext_code%20stock_status%20price_range%7Bminimum_price%7Bregular_price%7Bvalue%20currency%20__typename%7Dfinal_price%7Bvalue%20currency%20__typename%7Dprice_promo_text%20msrp_price%7Bvalue%20currency%20__typename%7Ddiscount_on_msrp%7Bamount_off%20percent_off%20__typename%7Dplp_price%7Bwas_price%20now_price%20discount%20promotext_value%20has_coupon%20__typename%7D__typename%7D__typename%7Dbrand_name%20name_wout_brand%20manufacturer%20special_price%20sku%20small_image%7Burl%20sizes%7Bimage_id%20url%20__typename%7D__typename%7Durl_key%20is_preowned%7Dpage_info%7Btotal_pages%20current_page%20__typename%7Dtotal_count%20__typename%7D%7D&operationName=category&variables=%7B%22currentPage%22%3A{page}%2C%22id%22%3A{category_id}%2C%22idNum%22%3A{category_id}%2C%22onServer%22%3Atrue%2C%22pageSize%22%3A60%2C%22filter%22%3A%7B%22category_id%22%3A%7B%22eq%22%3A%22{category_id}%22%7D%7D%2C%22sort%22%3A%7B%7D%7D'
            response = requests.get(url, headers=headers)
            json_result = response.json()
            results = []

            for product_info in json_result['data']['products']['items']:
                k = 0
                while k < 5:
                    try:
                        url = f'https://www.jomashop.com/graphql?query=query%20productDetail(%24urlKey%3AString%2C%24onServer%3ABoolean\u0021)%7BproductDetail%3Aproducts(filter%3A%7Burl_key%3A%7Beq%3A%24urlKey%7D%7D)%7Bitems%7B__typename%20id%20sku%20name%20name_wout_brand%20on_hand_priority_text%20on_hand_priority%20is_preowned%20brand_name%20brand_url%20manufacturer%20url_key%20stock_status%20out_of_stock_template%20out_of_stock_template_text%20price_promo_text%20promotext_code%20promotext_type%20promotext_value%20shipping_availability%20is_shipping_free_message%20shipping_question_mark_note%20model_id%20image%7Blabel%20url%20__typename%7Dupc_code%20item_variation%20media_gallery%7B...%20on%20ProductImage%7Blabel%20role%20url%20sizes%7Bimage_id%20url%20__typename%7Durl_nocache%20__typename%7D__typename%7Dbreadcrumbs%7Bpath%20categories%7Bname%20url_key%20__typename%7D__typename%7Dreview_details%7Breview_summary%20review_count%20__typename%7Drating_configurations%7Brating_attributes%20__typename%7Dshort_description%7Bhtml%20__typename%7Ddescription%7Bhtml%20__typename%7Dmoredetails%7Bdescription%20more_details%7Bgroup_id%20group_label%20group_attributes%7Battribute_id%20attribute_label%20attribute_value%20__typename%7D__typename%7D__typename%7Dmsrp%20price_range%7Bminimum_price%7Bregular_price%7Bvalue%20currency%20__typename%7Dfinal_price%7Bvalue%20currency%20__typename%7Dprice_promo_text%20msrp_price%7Bvalue%20currency%20__typename%7Ddiscount_on_msrp%7Bamount_off%20percent_off%20__typename%7Ddiscount%7Bamount_off%20percent_off%20__typename%7D__typename%7D__typename%7Dcategories%7Bbreadcrumbs%7Bcategory_id%20category_name%20__typename%7D__typename%7D...%20on%20GroupedProduct%7Bitems%7Bqty%20position%20product%7Bid%20sku%20stock_status%20name%20brand_name%20name_wout_brand%20manufacturer%20manufacturer_text%20is_shipping_free_message%20shipping_availability%20url_key%20is_preowned%20preowned_item_condition%20preowned_item_condition_text%20preowned_box%20preowned_papers%20preowned_papers_year%20preowned_condition_description%20on_hand_priority_text%20on_hand_priority%20shipping_question_mark_note%20model_id%20msrp%20price_range%7Bminimum_price%7Bregular_price%7Bvalue%20currency%20__typename%7Dfinal_price%7Bvalue%20currency%20__typename%7Dprice_promo_text%20msrp_price%7Bvalue%20currency%20__typename%7Ddiscount_on_msrp%7Bamount_off%20percent_off%20__typename%7Ddiscount%7Bamount_off%20percent_off%20__typename%7D__typename%7D__typename%7Dmedia_gallery%7B...%20on%20ProductImage%7Blabel%20role%20url%20sizes%7Bimage_id%20url%20__typename%7Durl_nocache%20__typename%7D__typename%7Dmoredetails%7Bdescription%20__typename%7D__typename%7D__typename%7D__typename%7D...%20on%20ConfigurableProduct%7Bconfigurable_options%7Battribute_code%20attribute_id%20id%20label%20values%7Bdefault_label%20label%20store_label%20use_default_value%20value_index%20swatch_data%7Btype%20value...%20on%20ImageSwatchData%7Bthumbnail%20__typename%7D__typename%7D__typename%7D__typename%7Dvariants%7Battributes%7Bcode%20value_index%20label%20__typename%7Dproduct%7Bid%20brand_name%20brand_url%20brand_size%20manufacturer%20shipping_availability%20is_shipping_free_message%20shipping_question_mark_note%20name_wout_brand%20msrp%20price_promo_text%20promotext_code%20promotext_type%20promotext_value%20is_preowned%20model_id%20on_hand_priority_text%20on_hand_priority%20price_range%7Bminimum_price%7Bregular_price%7Bvalue%20currency%20__typename%7Dfinal_price%7Bvalue%20currency%20__typename%7Dprice_promo_text%20msrp_price%7Bvalue%20currency%20__typename%7Ddiscount_on_msrp%7Bamount_off%20percent_off%20__typename%7Ddiscount%7Bamount_off%20percent_off%20__typename%7D__typename%7D__typename%7Dmedia_gallery%7B...%20on%20ProductImage%7Blabel%20role%20url%20sizes%7Bimage_id%20url%20__typename%7Durl_nocache%20__typename%7D__typename%7Dsku%20stock_status%20moredetails%7Bdescription%20__typename%7D__typename%7D__typename%7D__typename%7D...%20on%20GiftCardProduct%7Ballow_open_amount%20open_amount_min%20open_amount_max%20giftcard_type%20is_redeemable%20lifetime%20allow_message%20message_max_length%20giftcard_amounts%7Bvalue_id%20website_id%20website_value%20attribute_id%20value%20__typename%7D__typename%7Dmeta_title%40include(if%3A%24onServer)meta_keyword%40include(if%3A%24onServer)meta_description%40include(if%3A%24onServer)canonical_url%40include(if%3A%24onServer)%7D__typename%7D%7D&operationName=productDetail&variables=%7B%22urlKey%22%3A%22{product_info["url_key"]}%22%2C%22onServer%22%3Atrue%7D'
                        response = requests.get(url, headers=headers)
                        datajson = response.json()['data']['productDetail']['items'][0]
                        if datajson['stock_status'] == 'OUT_OF_STOCK':
                            break
                        j = 0
                        while j < 2:
                            pr_obj = get_product_detail(data=datajson, category_name=category_name, cnt=j)
                            if pr_obj:
                                results.append(pr_obj)
                                j += 1
                        break
                    except Exception as e:
                        k += 1
                        print(e)
                        time.sleep(5)
            return results
        except Exception as e:
            print(e, data)
            i += 1
            time.sleep(5)


def get_product_detail(data, category_name, cnt):
    gender = ''
    for more_detail in data['moredetails']['more_details']:
        if more_detail['group_label'] == 'Information':
            for group_attribute in more_detail['group_attributes']:
                if group_attribute['attribute_id'] == 'gender':
                    gender = group_attribute['attribute_value']

    color = ''
    for more_detail in data['moredetails']['more_details']:
        if more_detail['group_label'] == 'Information':
            for group_attribute in more_detail['group_attributes']:
                if group_attribute['attribute_label'] == 'Color':
                    color = group_attribute['attribute_value']

    more_detail_text = ''
    for more_detail in data['moredetails']['more_details']:
        more_detail_text += """<div class="more-detail-Row">"""
        more_detail_text += '<h3 class="more-detail-head">' + more_detail['group_label'] + '</h3>'
        for group_attribute in more_detail['group_attributes']:
            more_detail_text += '<div class="more-detail-content">'
            more_detail_text += f'<h4 class="more-label">{group_attribute["attribute_label"]}</h4>'
            more_detail_text += f'<span class="more-value">{group_attribute["attribute_label"]}</span>'
            more_detail_text += '</div>'
        more_detail_text += "</div>"
    # 'serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'condition', 'ticker', 'StyleId',
    # 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
    # 'name_en', "original_price", 'retail_price', 'whole_sale_price', 'description_en', 'gender',
    # 'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material',
    # 'origin', 'size_slug',
    # 'description_plain_en', 'delivery_information', 'main_pic',
    if cnt == 0:
        serial_no = str(data['id']) + 'AED'
        price = (50 + (data['price_range']['minimum_price']['msrp_price']['value'] * 1.13)) * 4.86
    else:
        serial_no = str(data['id']) + 'KSA'
        price = ((((50 + (data['price_range']['minimum_price']['msrp_price']['value'] * 1.13)) * 4.86) * 10) / 100) + (50 + (data['price_range']['minimum_price']['msrp_price']['value'] * 1.13)) * 4.86
    obj = {
        'serial_no': serial_no,
        'ref':TS,
        # 'product_link': f'https://www.jomashop.com/{data["canonical_url"]}',
        'group_sku': data['sku'].replace('-', ''),
        'product_sku': data['sku'].replace('-', ''),
        'brand': data['brand_name'],
        'category': category_name,
        'gender': gender,
        'name_en': data['name_wout_brand'],
        'description_en': data['moredetails']['description'],
        'description_plain_en': data['moredetails']['description'],
        # 'details': more_detail_text,
        "original_price": data['price_range']['minimum_price']['msrp_price']['value'],
        'whole_sale_price': price,
        'size_slug': 'US',
        'retail_price': price,
        # 'discounted price': f"{data['price_range']['minimum_price']['final_price']['value']} {data['price_range']['minimum_price']['final_price']['currency']}",
        'color': color,
        'quantity': data['stock_status'],
        'main_pic': data['image']['url'],
        'delivery_information': '15 to 20 days'
    }
    index = 0
    try:
        for dt in data['variants']:
            if dt['product']['stock_status'] == 'OUT_OF_STOCK':
                continue
            obj[f'variant_{index + 1}'] = dt['attributes'][0]['label'].split(':')[-1].split()[0]
            try:
                obj[f'variant_{index + 1}_price'] = dt['product']['price_range']['minimum_price']['final_price']['value']
            except:
                obj[f'variant_{index + 1}_price'] = dt['product']['price_range']['minimum_price']['regular_price']['value']
            index += 1
    except:
        obj[f'variant_1'] = data['name'].split('Brand')[-1].split()[1]
        try:
            obj[f'variant_1_price'] = data['price_range']['minimum_price']['final_price']['value']
        except:
            obj[f'variant_1_price'] = data['price_range']['minimum_price']['regular_price']['value']

    image_count = 1
    while image_count < 10 and image_count < (len(data['media_gallery']) + 1):
        obj[f'pic_{image_count}'] = data['media_gallery'][image_count - 1]['url_nocache']
        image_count += 1
    return obj


if __name__ == '__main__':
    ct = datetime.datetime.now()
    TS = str(ct.timestamp()).replace('.', '')
    print('---------- Start -----------')
    cat_file = open('Categories.txt', 'r')
    categories = cat_file.read().split('\n')
    for category_url in categories:
        cateresult = get_category_info(category_url)

        inputs = []
        for page in range(1, cateresult['total_page'] + 1):
            inputs.append({
                'category_id': cateresult['category_id'],
                'page': page,
                'category_name': cateresult['category_name']
            })

        # exec = concurrent.futures.ThreadPoolExecutor(20)
        # results = exec.map(crawl_product_for_page(inputs))
        # for input in inputs:
        #     results = crawl_product_for_page(input)
        #     for result in results:
        #         order = sorted(result.keys())
        #         for key in order:
        #             row += 1
        #             worksheet.write(row, col, key)
        #             i = 1
        #             # for item in result[key]:
        #             worksheet.write(row, col + i, result[key])
        #
        #             # i += 1
        # for input in inputs:
        #     results = crawl_product_for_page(input)
        #     for res in results:
        #         writer.writerow(res)
        #         csvfile.flush()
        with concurrent.futures.ThreadPoolExecutor(20) as exec:
            results = exec.map(crawl_product_for_page, inputs)
            for result in results:
                if result:
                    writer.writerows(result)
                    csvfile.flush()
