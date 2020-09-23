"""
This file scrape fights information from tapology.com
"""
import copy
import csv
import json
import logging
import time

import scrapy

from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options as ff_options
import requests

logging.basicConfig(filename='tapology.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

csv_columns = ['name_on_ufc', 'url', 'Location', 'date', 'left_fighter', 'right_fighter', 'left_odds', 'right_odds',
               'left_weight', 'right_weight', 'left_age', 'right_age', 'left_height',
               'right_height', 'left_reach', 'right_reach', 'left_gym', 'right_gym',
               'left_nationality', 'right_nationality', 'right_pro_record', 'left_pro_record', 'event']
csvfile = open('tapology.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
}
headers_3 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Cookie': '_ga=GA1.2.384393748.1592152527; _gid=GA1.2.1189371252.1592371180; '
              '_tapology_mma_session'
              '=ZUdaRGwzWXZvNVZBbWpUYVFXdkNINSs4MGsvdjRheUJkWmJ3cmUyckJ3NlBQN0x5cCtBYW9CZDRRWkJ4c3V0ZHFTQ1J1SUR1TzZRRzVPRngzdHdkS2lMUUVlVkhUYnNIZG9IVWlDTGFmZGZZMC9qV1dEMHRmdmwyUmpiUWxaWXFXU2tBM0V3T29iQklVOStoTkdqMlFxL0FBY3NBNjIwd3NvTlRVc1N3Q0xVUjFHMUY0dVRJRERScUp6S2EwbHBZLS1XaFJDM0x3cy9jM1ZlaGltVHgrcmxRPT0%3D--8eb0ab07c54255732e8ef0ce204cd3e5842473ea',
    'Host': 'www.tapology.com',
    'If-None-Match': 'W/"a9f4e58b7d264e703f4dc4f0ca51fc36"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}
data_template = {
    'view_name': 'all_athletes',
    'view_display_id': 'page',
    'view_base_path': '',
    'pager_element': 0,
    'filters%5B0%5D': 'status%3A23',
    'gender': 'All',
    'page': '0'
}


def get_age(age):
    """
    this function calculates age of athlete in months
    :param age:
    :return:
    """
    try:
        if 'month' in age:
            age = age.replace('year', '').replace('month', '').replace('day', '').replace('s', '')
            age = age.split(',')
            return (int(age[0].strip()) * 12) + int(age[1].strip())
        else:
            age = age.replace('year', '').replace('day', '').replace('s', '')
            age = age.split(',')
            return int(age[0].strip()) * 12
    except:
        return None


def get_height_reach(value):
    """
    this function returns height of athlete in lbs
    :param value:
    :return:
    """
    if value:
        try:
            return value.split()[1].replace('(', '').replace(')', '').replace('cm', '').strip()
        except:
            return None
    else:
        return None


def get_all_players():
    """
    This function scrapes information from tapology.com
    :return:
    """
    f = open("tapology_links.txt", "r")
    data = f.read()
    for fight_data in [v for v in list(set(data.split('\n'))) if v]:
        athlete_name = fight_data.split(': ')[0].strip()
        link = fight_data.split(': ')[1].strip()
        logging.warning('getting fight: {}'.format(link))
        print('getting fight: {}'.format(link))
        # time.sleep(3)
        try:
            resp = requests.get(link, headers=headers_3, proxies={'https': 'https://5.79.73.131:13010'})  # get fight response from tapology.com
        except:
            try:
                resp = requests.get(link, headers=headers_3, proxies={
                    'https': 'https://5.79.73.131:13010'})  # get fight response from tapology.com
            except:
                continue
        response = scrapy.Selector(text=resp.content.decode('utf-8'))
        item = dict()
        item['name_on_ufc'] = athlete_name.strip()
        item['url'] = link
        for li in response.css('ul.clearfix li'):
            if 'event' in li.css('strong ::text').extract_first('').lower():
                item['event'] = li.css('span ::text').extract_first('')
            if 'location' in li.css('strong ::text').extract_first('').lower():
                item['Location'] = li.css('span ::text').extract_first('')
            if 'date' in li.css('strong ::text').extract_first('').lower():
                item['date'] = li.css('span ::text').extract_first('').split()[1].replace('.', '/')
        item['left_fighter'] = response.css('.fName.left a ::text').extract_first()
        item['right_fighter'] = response.css('.fName.right a ::text').extract_first()
        for tr in response.css('.fighterStats.spaced tr'):
            if 'odd' in tr.css('.category ::text').extract_first('').lower():
                item['left_odds'] = tr.css('td')[0].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[0].css('::text').extract_first('').strip() else None
                item['right_odds'] = tr.css('td')[-1].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[-1].css('::text').extract_first('').strip().split() else None
            if 'pro ' in tr.css('.category ::text').extract_first('').lower():
                item['left_pro_record'] = tr.css('td')[0].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[0].css('::text').extract_first('').strip() else None
                item['right_pro_record'] = tr.css('td')[-1].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[-1].css('::text').extract_first('').strip().split() else None
            if 'weigh' in tr.css('.category ::text').extract_first('').lower():
                item['left_weight'] = tr.css('td')[0].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[0].css('::text').extract_first('').strip().split() else None
                item['right_weight'] = tr.css('td')[-1].css('::text').extract_first('').strip().split()[0] if \
                tr.css('td')[-1].css('::text').extract_first('').strip().split() else None
            if 'age' in tr.css('.category ::text').extract_first('').lower():
                item['left_age'] = get_age(tr.css('td')[0].css('::text').extract_first('').strip())
                item['right_age'] = get_age(tr.css('td')[-1].css('::text').extract_first('').strip())
            if 'height' in tr.css('.category ::text').extract_first('').lower():
                item['left_height'] = get_height_reach(tr.css('td')[0].css('::text').extract_first('').strip())
                item['right_height'] = get_height_reach(tr.css('td')[-1].css('::text').extract_first('').strip())
            if 'reach' in tr.css('.category ::text').extract_first('').lower():
                item['left_reach'] = get_height_reach(tr.css('td')[0].css('::text').extract_first('').strip())
                item['right_reach'] = get_height_reach(tr.css('td')[-1].css('::text').extract_first('').strip())
            if 'gym' in tr.css('.category ::text').extract_first('').lower():
                item['left_gym'] = tr.css('td')[0].css('::text').extract_first('').strip() or ' and '.join(
                    tr.css('td')[0].css(' a::text').extract())
                item['right_gym'] = tr.css('td')[-1].css('::text').extract_first('').strip() or ' and '.join(
                    tr.css('td')[-1].css(' a::text').extract())
            if 'national' in tr.css('.category ::text').extract_first('').lower():
                item['left_nationality'] = ''.join(tr.css('td')[0].css('::text').extract()).strip()
                item['right_nationality'] = ''.join(tr.css('td')[-1].css('::text').extract()).strip()
        try:
            writer.writerow(item)  # write fight data to tapology.csv
            csvfile.flush()
        except Exception as e:
            print(str(e))
            pass


if __name__ == '__main__':
    # if you have any proxy replace "None" in next line with that proxy

    get_all_players()
