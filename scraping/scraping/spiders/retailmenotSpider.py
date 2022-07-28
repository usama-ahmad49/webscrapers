try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import csv
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

new_file_num = 0


def file_input_func():
    file_input = open('input_retailmenotSpider.txt', 'r')
    input_list = file_input.read()
    return input_list.split('\n')


def links_from_existing_file():
    global new_file_num
    files_arr = os.listdir('.')
    files_with_same_name = [s for s in files_arr if 'retailmenotSpider_' in s]
    fl_list = []
    for f in files_with_same_name:
        fl = (f.split('_')[1]).split('.')[0]
        fl_list.append(fl)
    if fl_list.__len__() != 0:
        new_file_num = int(max(fl_list))
    else:
        return
    read_links = open('retailmenotSpider_{}.csv'.format(new_file_num), 'r')
    links_exist = read_links.read().split('\n')
    for l in links_exist[1:-1]:
        try:
            l = l.split(',')
            existing_link = l[1]
        except:
            continue
        existing_link_list.append(existing_link)


def get_dict_value(data, key_list, default=''):
    """
    gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
    :param data: dictionary
    :param key_list: list of key
    :param default: return value if key not found
    :return:
    """
    for key in key_list:
        if data and isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def get_link(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    try:
        category = ','.join(driver.find_element_by_class_name('Breadcrumbs__StyledNav-nw36dv-0.dIZdOC').text.split('›')[1:-1])
    except:
        category = ''
    get_json_from_page = driver.find_element_by_id('__NEXT_DATA__')
    json_text = get_json_from_page.get_attribute('innerHTML')
    json_data_parsed = json.loads(json_text)
    oc_list = []
    data = get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data'], [])

    try:
        ocs = [v for v in data.values() if 'offers' in v.keys() and v.get('type') == 'top-rated'][0].get('offers')
    except:
        try:
            ocs = [v for v in data.values() if 'offers' in v.keys()][-1].get('offers')
        except:
            return

    for oc in ocs:
        code = oc.get('id')
        oc_list.append(code)
    for offer_code in oc_list:
        item = dict()
        if len((url.split('/')[4].replace('.com','')).split('.')) == 1:
            item['shop name'] = url.split('/')[4].replace('.com','')
        else:
            item['shop name'] = (url.split('/')[4].replace('.com', '')).split('.')[1]

        try:
            if '/out/O/' in get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code + '.redemption.0.windowMagic.1', 'url']):
                item['affiliate link'] = 'https://www.retailmenot.com{}'.format(get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code + '.redemption.0.windowMagic.1', 'url']))
            else:
                item['affiliate link'] = 'https://www.retailmenot.com{}'.format(get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code + '.redemption.0.windowMagic.0', 'url']))
        except:
            item['affiliate link'] = ''
        if item['affiliate link'] in existing_link_list:
            continue
        currentdate = datetime.now()
        newDate = currentdate + relativedelta(weeks=1)
        item['expiry date'] = newDate.strftime('%m,%d,%Y')
        if get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code + '.redemption.0', 'code']):
                item['type'] = 'coupon'
        else:
            item['type'] = 'sale'
        try:
            item['code']=get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code + '.redemption.0', 'code'])
        except:
            item['code']=''
        try:
            item['title'] = get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code, 'title'])
        except:
            item['title'] = ''

        try:
            item['description'] = get_dict_value(json_data_parsed, ['props', 'pageProps', 'serverState', 'apollo', 'data', offer_code, 'description'])
        except:
            item['description'] = ''
        item['logo'] = ''.join(item['shop name'].split()).lower()
        writer.writerow(item)
        fileout.flush()
    print('site done: ' + url)
    driver.close()


if __name__ == '__main__':
    existing_link_list = []
    inputs = file_input_func()
    links_from_existing_file()
    header = ['shop name', 'affiliate link', 'expiry date', 'type', 'code', 'title', 'description','logo']
    fileout = open('retailmenotSpider_{}.csv'.format(str(new_file_num + 1)), 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(fileout, fieldnames=header)
    writer.writeheader()

    for link in inputs:
        get_link(link)
