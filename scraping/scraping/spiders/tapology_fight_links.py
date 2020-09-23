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

file1 = open("tapology_links.txt", "a")
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
}
headers_3 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': '_ga=GA1.2.384393748.1592152527; _gid=GA1.2.1189371252.1592371180; _tapology_mma_session=ZUdaRGwzWXZvNVZBbWpUYVFXdkNINSs4MGsvdjRheUJkWmJ3cmUyckJ3NlBQN0x5cCtBYW9CZDRRWkJ4c3V0ZHFTQ1J1SUR1TzZRRzVPRngzdHdkS2lMUUVlVkhUYnNIZG9IVWlDTGFmZGZZMC9qV1dEMHRmdmwyUmpiUWxaWXFXU2tBM0V3T29iQklVOStoTkdqMlFxL0FBY3NBNjIwd3NvTlRVc1N3Q0xVUjFHMUY0dVRJRERScUp6S2EwbHBZLS1XaFJDM0x3cy9jM1ZlaGltVHgrcmxRPT0%3D--8eb0ab07c54255732e8ef0ce204cd3e5842473ea',
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


def search_athlete(url):
    """
    this function search athlete profile on tapology.com
    :param url:
    :return:
    """
    resp = requests.get(url, proxies={'https': 'https://5.79.73.131:13010'})
    response = scrapy.Selector(text=resp.content.decode('utf-8'))
    return 'https://www.tapology.com{}'.format(response.css('a ::attr(href)').extract_first(''))


def create_driver(random_proxy, user_agent, for_headers=False, webrtc=True):
    """
    creates firefox or chrome driver with given settings
    :param random_proxy:
    :param user_agent:
    :param for_headers:
    :param webrtc:
    :return:
    """
    options = ff_options()
    # options.add_argument('--headless')
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    if random_proxy:
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": random_proxy,
            "ftpProxy": random_proxy,
            "sslProxy": random_proxy
        }
    driver = webdriver.Firefox(executable_path='C:\Windows\geckodriver', firefox_options=options,
                               capabilities=firefox_capabilities)
    return driver


def get_athlete_fights(athlete_link):
    """
    open athlete link in chrome to get his fight links
    :param athlete_link: link of athlete's profile
    :return:
    """
    logging.warning('opening in chrome: {}'.format(athlete_link))
    print('opening in chrome: {}'.format(athlete_link))
    if athlete_link == 'https://www.tapology.com/' or athlete_link == 'https://www.tapology.com':
        return []
    try:
        driver.set_page_load_timeout(60)
        driver.get(athlete_link)
    except:
        pass
    time.sleep(20)
    response = scrapy.Selector(text=driver.page_source)
    fight_links = []
    for li in response.css('.fighterFightResults ul li'):
        if 'ufc' in li.css('.notes a ::text').extract_first('').lower():
            fight_links.append(li.css('.lead a ::attr(href)').extract_first(''))
    return fight_links


def get_all_players():
    """
    This function scrapes information from tapology.com
    :return:
    """

    #   code to get athelete names from ufc.com
    data = copy.deepcopy(data_template)
    url = 'https://www.ufc.com/views/ajax?filters%5B0%5D=status%3A23&_wrapper_format=drupal_ajax'
    athlete_names = []
    page = 0
    while True:
        data['page'] = str(page)
        page += 1
        resp = requests.post(url, headers=headers, data=data)
        response_data = json.loads(resp.content.decode('utf-8'))
        response = scrapy.Selector(text=response_data[-1].get('data'))
        if not response.css('.e-button--black ::attr(href)').extract():
        # if not response.css('.e-button--black ::attr(href)').extract() or len(athlete_names) > 1:     # if you want to extract 10 athletes data then uncomment this line and comment above line
            break
        athlete_names.extend(response.css('.c-listing-athlete__name ::text').extract())
        # time.sleep(3)
    # athlete_names = All athlete names on ufc.com
    reversed(athlete_names)
    for athlete_name in athlete_names:
        url = 'https://www.tapology.com/search/nav?ajax=true&model=fighters&term={}'.format(
            athlete_name.strip().replace(' ', '%20'))
        try:
            athlete_link = search_athlete(url)  # search athlete on tapology.com
        except:
            continue
        for link in list(set(get_athlete_fights(athlete_link))):
            print('{}: {}'.format(athlete_name.strip(), link))
            file1.write('{}: {}\n'.format(athlete_name.strip(), link))


if __name__ == '__main__':
    # if you have any proxy replace "None" in next line with that proxy
    driver = (create_driver('5.79.73.131:13010',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'))
    get_all_players()
    driver.close()
