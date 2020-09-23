try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import json
import random
import time

import googlemaps
import requests
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ch_options
import urllib.request
from PIL import Image
from selenium.webdriver.common.proxy import Proxy, ProxyType

csv_columns = ['url', 'phone', 'title', 'address', 'lat', 'lng', 'votes', 'rating', 'Established', 'imgPaths']
csvfile = open('justdial.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()
gmaps = googlemaps.Client(key='AIzaSyCjzKQmZwR2OYbodDtZXtEH1klDuT6pols')


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


def get_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    driver = webdriver.Firefox(firefox_options=options)
    return driver


def get_shop_links(link, driver):
    driver.get(link)
    scroll_pause_time = 5
    last_height = driver.execute_script("return document.body.scrollHeight")
    # count = 0
    while True:
        # count += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    response = scrapy.Selector(text=driver.page_source)
    return response.css('h2.store-name a::attr(href)').extract()


def ocr_space_file(filename, overlay=False, language='eng'):
    f2 = open("image_key.txt", "r")
    keys = f2.read()
    if keys:
        keys = keys.split()
    api_key = random.choice(keys)
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return json.loads(r.content.decode())['ParsedResults'][0]['ParsedText'].strip()


def get_shop_data(link, driver):
    driver.get(link)
    time.sleep(1)

    response = scrapy.Selector(text=driver.page_source)
    item = dict()
    item['title'] = response.css('.rstotle .fn::text').extract_first('')
    driver.get_screenshot_as_file("SS.png")
    img = Image.open("SS.png")
    region = img.crop((30, 175, 630, 250))
    region.save("region.png")
    try:
        text = ocr_space_file(filename='region.png', language='pol')
    except:
        text = ''
    item['phone'] = text.split('\n')[1] if 'Map' in text else text
    item['address'] = response.css('#fulladdress span span::text').extract_first()
    geocode_result = gmaps.geocode(item['address'])
    item['lat'] = ''
    item['lng'] = ''
    try:
        item['lat'] = geocode_result[0]['geometry']['location']['lat']
        item['lng'] = geocode_result[0]['geometry']['location']['lng']
    except:
        pass
    item['url'] = link
    item['votes'] = response.css('#totrat ::attr(value)').extract_first('')
    item['rating'] = response.css('.value-titles ::text').extract_first('')
    item['Established'] = response.css('ul.alstdul li ::text').extract()[-1] if response.css(
        'ul.alstdul li ::text').extract() else ''
    img_paths = []
    img_links = response.css('.catyimgul img ::attr(src)').extract()
    if '==' in response.css('.catyimgul a.e_prop ::attr(href)').extract()[-1]:
        driver.quit()
        options_ch = ch_options()
        options_ch.add_argument('--disable-notifications')
        driver = webdriver.Chrome(chrome_options=options_ch)
        driver.get(response.css('.catyimgul a.e_prop ::attr(href)').extract()[-1])
        time.sleep(2)
        img_resp = scrapy.Selector(text=driver.page_source)
        img_links = img_resp.css('.gall_pic img ::attr(data-src)').extract()
        img_links.extend(img_resp.css('.gall_pic img ::attr(src)').extract())
    for img_link in img_links[:10]:
        print('downloading image: {}'.format(img_link))
        try:
            urllib.request.urlretrieve(img_link, "pictures/{}.jpg".format(img_link.split('/')[-1]))
            img_paths.append("pictures/{}.jpg".format(img_link.split('/')[-1]))
        except:
            try:
                urllib.request.urlretrieve(img_link, "pictures/{}".format(img_link.split('/')[-1].split('?')[0]))
                img_paths.append("pictures/{}".format(img_link.split('/')[-1].split('?')[0]))
            except:
                pass
    item['imgPaths'] = img_paths

    writer.writerow(item)
    csvfile.flush()
    driver.quit()


if __name__ == '__main__':
    states = ['Delhi', 'Ahmedabad', 'Bangalore', 'Chandigarh', 'Chennai', 'Coimbatore', 'Goa', 'Gurgaon', 'Hyderabad',
              'Indore', 'Jaipur', 'Lolkata', 'Mumbai', 'Noida', 'Pune']
    f = open("justdial_input.txt", "r")
    state_input = f.read()
    if state_input:
        states = state_input.split()
    driver = get_driver()
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "ip_addr:port"
    # prox.socks_proxy = "ip_addr:port"
    # prox.ssl_proxy = "ip_addr:port"
    #
    # capabilities = webdriver.DesiredCapabilities.FIREFOX
    # prox.add_to_capabilities(capabilities)

    # driver = webdriver.Chrome(desired_capabilities=capabilities)
    for state in states:
        print('getting state: {}'.format(state))
        state = camelCase(state)
        # shop_links = get_shop_links('https://www.justdial.com/{}/search?q=Jewellery-Showrooms'.format(state), driver)
        # for shop_link in shop_links:
        #     print('getting shop: {}'.format(shop_link))
        #     options_ch = ch_options()
        #     options_ch.add_argument('--disable-notifications')
        #     driver_chrome = webdriver.Chrome(chrome_options=options_ch)
        #     get_shop_data(shop_link, driver_chrome)
        for page_number in range(6, 50):
            driver.quit()
            driver = get_driver()
            state = camelCase(state)
            shop_links = get_shop_links('https://www.justdial.com/{}/Jewellery-Showrooms/nct-10282098/page-{}'.format(state, page_number),
                                        driver)
            for shop_link in shop_links:
                print('getting shop: {}'.format(shop_link))
                options_ch = ch_options()
                options_ch.add_argument('--disable-notifications')
                driver_chrome = webdriver.Chrome(chrome_options=options_ch)
                get_shop_data(shop_link, driver_chrome)

    driver.close()
