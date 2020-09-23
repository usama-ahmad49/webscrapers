try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import os
import csv
import json
import time

import requests
import scrapy
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def do_scroll(driver):
    scroll_pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver


def get_dict_value(data, key_list, default=''):
    for key in key_list:
        if data and isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def get_hotel_data(hotel_link,categoryDict):
    driver_hotel = webdriver.Firefox()
    driver_hotel.maximize_window()
    actions = ActionChains(driver_hotel)
    key='pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMlNhbnRhJTIwQ3J1eiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpTZFUyZkJ0RWpvQVJoZm5YS2tzUXlsSSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNi45NzQxMTcwOTk5OTk5OSUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjIuMDMwNzk2MyU3RA%3D%3D'
    hotel_link = 'https://www.ubereats.com{}?{}'.format(hotel_link,key)
    # hotel_link = 'https://www.ubereats.com/san-francisco/food-delivery/jack-in-the-box-444-640-ocean/MXzcCgMSQSKSc-xjW4SORg?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMlNhbnRhJTIwQ3J1eiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpTZFUyZkJ0RWpvQVJoZm5YS2tzUXlsSSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNi45NzQxMTcwOTk5OTk5OSUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjIuMDMwNzk2MyU3RA%3D%3D'
    driver_hotel.get(hotel_link)
    time.sleep(3)
    if driver_hotel.find_elements_by_css_selector(
            '#wrapper > div:nth-child(5) > div > div > div.ap.af.at > div.h0.ba.h1.dp.fw > button'):
        driver_hotel.find_element_by_css_selector(
            '#wrapper > div:nth-child(5) > div > div > div.ap.af.at > div.h0.ba.h1.dp.fw > button').click()
    time.sleep(5)
    absolutepath = os.path.dirname(os.path.abspath(__file__))
    for menu_item in driver_hotel.find_elements_by_tag_name('main ul li')[:30]:
        try:
            actions.move_to_element(menu_item).perform()
            menu_item.click()
            time.sleep(2)
            webdriver.ActionChains(driver_hotel).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
        except:
            continue

    all_data = [v for v in driver_hotel.requests if 'api/getMenuItemV1' in v.path]
    hotel_response = scrapy.Selector(text=driver_hotel.page_source)
    hotel_name = hotel_response.css('h1 ::text').extract_first('').encode('ascii','ignore').decode('utf-8')

    path = absolutepath +'\{}Datafolder'.format(hotel_name)
    try:
        os.mkdir(path)
    except OSError:
        print('creation of folder failed')
    csv_columns_catagory = ['Category Name*', 'Parent Category Id', 'Category Description', 'Category Image Url',
                            'taxId', 'Side Order', 'Category Id', 'Enable', 'Delete', 'Category Name English',
                            'Category Name Arabic', 'Category Name French', 'Category Name Spanish',
                            'Category Name Malay', 'Category Name Chinese Simplified', 'Category Name Portuguese',
                            'Category Name Chinese Traditional', 'Category Name Bengali',
                            'Category Name Mexican Spanish', 'Category Name Khmer', 'Category Name Tamil',
                            'Category Name Sinhala', 'Category Name Swedish', 'Category Name Greek',
                            'Category Name Dutch', 'Category Name Korean', 'Category Name Brazilian Portuguese',
                            'Description English', 'Category Description Arabic', 'Category Description French',
                            'Category Description Spanish', 'Category Description Malay',
                            'Category Description Chinese Simplified', 'Category Description Portuguese',
                            'Category Description Chinese Traditional', 'Category Description Bengali',
                            'Category Description Mexican Spanish', 'Category Description Khmer',
                            'Category Description Tamil', 'Category Description Sinhala',
                            'Category Description Swedish', 'Category Description Greek', 'Category Description Dutch',
                            'Category Description Korean', 'Category Description Brazilian Portuguese']
    csv_columns_addon = ['Product Id*', 'Addon Id', 'Addon Name*', 'Multi Select*', 'Addon Option Id',
                         'Addon Option Name*', 'Price*', 'Default*', 'Addon Name English', 'Addon Name Arabic',
                         'Addon Name French', 'Addon Name Spanish', 'Addon Name Malay', 'Addon Name Chinese Simplified',
                         'Addon Name Portuguese', 'Addon Name Chinese Traditional', 'Addon Name Bengali',
                         'Addon Name Mexican Spanish', 'Addon Name Khmer', 'Addon Name Tamil', 'Addon Name Sinhala',
                         'Addon Name Swedish', 'Addon Name Greek', 'Addon Name Dutch', 'Addon Option Korean',
                         'Addon Name Brazilian Portuguese', 'Addon Option Name English', 'Addon Option Name Arabic',
                         'Addon Option Name French', 'Addon Option Name Spanish', 'Addon Option Name Malay',
                         'Addon Option Name Chinese Simplified', 'Addon Option Name Portuguese',
                         'Addon Option Name Chinese Traditional', 'Addon Option Name Bengali',
                         'Addon Option Name Mexican Spanish', 'Addon Option Name Khmer', 'Addon Option Name Tamil',
                         'Addon Option Name Sinhala', 'Addon Option Name Swedish', 'Addon Option Name Greek',
                         'Addon Option Name Dutch', 'Addon Option Name Korean',
                         'Addon Option Name Brazilian Portuguese']
    csv_columns_productType = ['Product Name*', 'Product Price*', 'Category Id*', 'Product Description',
                               'Product Long Description', 'Product Image Url', 'taxId', 'Cost Price', 'MRP', 'SKU',
                               'Side Order', 'Product Id', 'Is Veg*', 'Available Quantity', 'Inventory*', 'Enable',
                               'Delete', 'Product Name English', 'Product Name Arabic', 'Product Name French',
                               'Product Name Spanish', 'Product Name Malay', 'Product Name Chinese Simplified',
                               'Product Name Portuguese', 'Product Name Chinese Traditional', 'Product Name Bengali',
                               'Product Name Mexican Spanish', 'Product Name Khmer', 'Product Name Swedish',
                               'Product Name Greek', 'Product Name Dutch', 'Product Name Korean',
                               'Product Name Brazilian Portuguese', 'Product Description English',
                               'Product Description Arabic', 'Product Description French',
                               'Product Description Spanish', 'Product Description Malay',
                               'Product Description Chinese Simplified', 'Product Description Portuguese',
                               'Product Description Chinese Traditional', 'Product Description Bengali',
                               'Product Description Mexican Spanish', 'Product Description Khmer',
                               'Product Description Swedish', 'Product Description Greek', 'Product Description Dutch',
                               'Product Description Korean', 'Product Description Brazilian Portuguese',
                               'Long Description English', 'Long Description Arabic', 'Long Description French',
                               'Long Description Spanish', 'Long Description Malay',
                               'Long Description Chinese Simplified', 'Long Description Portuguese',
                               'Long Description Chinese Traditional', 'Long Description Bengali',
                               'Long Description Mexican Spanish', 'Long Description Khmer', 'Long Description Swedish',
                               'Long Description Greek', 'Long Description Dutch', 'Long Description Korean',
                               'Long Description Brazilian Portuguese']
    csvfile_catagory = open('{}\{}_catagory_parser.csv'.format(path,hotel_name), 'w', newline='', encoding='utf-8')
    csvfile_addon = open('{}\{}_addon_parser.csv'.format(path,hotel_name), 'w', newline='', encoding='utf-8')
    csvfile_productType = open('{}\{}_productType_parser.csv'.format(path,hotel_name), 'w', newline='', encoding='utf-8')
    writer_cat = csv.DictWriter(csvfile_catagory, fieldnames=csv_columns_catagory)
    writer_cat.writeheader()
    writer_addon = csv.DictWriter(csvfile_addon, fieldnames=csv_columns_addon)
    writer_addon.writeheader()
    writer_product = csv.DictWriter(csvfile_productType, fieldnames=csv_columns_productType)
    writer_product.writeheader()

    itemcat = dict()
    i = 0
    while i != hotel_response.css('h2 ::text').extract().__len__():
        itemcat['Category Name*'] = hotel_response.css('h2 ::text').extract()[i]
        itemcat['Parent Category Id'] = ''
        itemcat['Category Description'] = ''
        itemcat['Category Image Url'] = ''
        itemcat['taxId'] = ''
        i = i + 1
        writer_cat.writerow(itemcat)
        csvfile_catagory.flush()

    for data in all_data:
        headers = dict(data.headers)
        body = data.body.decode('utf-8')
        try:
            time.sleep(3)
            resp = requests.post(data.path, data=body, headers=headers).text
            resp = json.loads(resp)
        except Exception as e:
            print(str(e))
            continue


        itemAddon = dict()
        itemProduct = dict()



        for addonInfo in get_dict_value(resp, ['data', 'customizationsList']):
            itemAddon['Product Id*'] = get_dict_value(resp, ['data', 'title'])
            itemAddon['Addon Id'] = get_dict_value(addonInfo, ['title'])
            itemAddon['Addon Name*'] = get_dict_value(addonInfo, ['title'])
            writer_addon.writerow(itemAddon)
            csvfile_addon.flush()

            for info in get_dict_value(addonInfo, ['options']):
                item_addon_sub = dict()
                item_addon_sub.update(itemAddon)
                item_addon_sub['Multi Select*'] = ''
                item_addon_sub['Addon Option Id'] = ''
                item_addon_sub['Addon Option Name*'] = get_dict_value(info, ['title'])
                addonprice=(float(get_dict_value(info, ['price'])))/float(100)
                item_addon_sub['Price*'] = '+ $'+ str(addonprice)
                item_addon_sub['Default*'] = str(get_dict_value(info, ['defaultQuantity']))
                writer_addon.writerow(item_addon_sub)
                csvfile_addon.flush()


        if(get_dict_value(resp, ['data','uuid']) in categoryDict.keys()):
            catagory_name =categoryDict[get_dict_value(resp, ['data', 'Uuid'])]
        else:
            catagory_name='nill'

        itemProduct['Product Name*'] = get_dict_value(resp, ['data', 'title'])
        productprice=(float(get_dict_value(resp, ['data', 'price'])))/float(100)
        itemProduct['Product Price*'] = '$' + str(productprice)
        itemProduct['Category Id*'] = catagory_name
        itemProduct['Product Description'] = get_dict_value(resp, ['data', 'itemDescription']).encode('ascii','ignore').decode('utf-8')
        itemProduct['Product Long Description'] = get_dict_value(resp, ['data', 'itemDescription']).encode('ascii','ignore').decode('utf-8')
        itemProduct['Product Image Url'] = get_dict_value(resp, ['data', 'imageUrl'])
        writer_product.writerow(itemProduct)
        csvfile_productType.flush()

    driver_hotel.quit()


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(
        'https://www.ubereats.com/feed?pl'
        '=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMlNhbnRhJTIwQ3J1eiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpTZFUyZkJ0RWpvQVJoZm5YS2tzUXlsSSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNi45NzQxMTcwOTk5OTk5OSUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjIuMDMwNzk2MyU3RA%3D%3D')
    time.sleep(5)
    driver = do_scroll(driver)
    complete = False
    while not complete:
        if driver.find_elements_by_xpath("//*[text()='Show more']"):
            driver.find_element_by_xpath("//*[text()='Show more']").click()
            time.sleep(10)
            driver = do_scroll(driver)
        else:
            complete = True
    response = scrapy.Selector(text=driver.page_source)
    all_D=[v for v in driver.requests if 'api/getSearchHomeV2' in v.path]
    catagoryDict={}
    for data in all_D:
        headers = dict(data.headers)
        body = data.body.decode('utf-8')
        try:
            time.sleep(3)
            resp2 = requests.post(data.path, data=body, headers=headers).text
            resp2 = json.loads(resp2)
        except Exception as e:
            print(str(e))
            continue
        for d in get_dict_value(resp2, ['data', 'suggestedSections'])[1]['items']:
            cat_dict = {get_dict_value(d, ['trackingCode'])['uuid']: get_dict_value(d, ['title'])}
            catagoryDict.update(cat_dict)

    for hotel_link in [v for v in response.css('main a ::attr(href)').extract() if 'search' not in v][2:]:
        try:
            get_hotel_data(hotel_link,catagoryDict)
        except:
            print('-: hotel {}: '.format(hotel_link))
            pass
    driver.quit()
