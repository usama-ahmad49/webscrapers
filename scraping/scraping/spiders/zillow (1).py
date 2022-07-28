try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import json
import random
import time
from threading import Thread

from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import AirtableZillow

basekey = 'appctQUT8ZpjYyfIJ'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'Zillow'

airtable_client = AirtableZillow.AirtableClient(apikey, basekey)

# headers_csv = ["ID","address", "zestimate", "rentZestimate", "lotAreaValue", "lotAreaUnit", "lot", "price", "beds", "baths",
#                "sqft", "yearBuilt", "phone"]
# fileout = open('zillow_data.csv', 'w', newline='', encoding='utf-8')
# writer = csv.DictWriter(fileout, fieldnames=headers_csv)
# writer.writeheader()
processed = []

def click_and_hold(driver, element):
    ActionChains(driver).click_and_hold(element).perform()

def get_proxy_dict():
    proxy_file = open('proxyzillow.txt', 'r')
    proxies = proxy_file.read().split('\n')
    proxies = [p for p in proxies if p.strip()]
    proxy = random.choice(proxies)
    proxies_dict = {
        'https': "https://{}".format(proxy),
        'http': "http://{}".format(proxy)
    }
    return proxies_dict


items_count = 1


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def make_request(url, headers, item):
    got = False
    while not got:
        try:
            resp = requests.post(url, data=json.dumps(req_body), headers=headers)
            property_data = json.loads(resp.text)
            # resp = requests.post(url, data=json.dumps(req_body), headers=headers, proxies=get_proxy_dict())
            if resp.status_code == 200:
                got = True
            else:
                print(resp.status_code)
                time.sleep(1)
        except Exception as e:
            print(str(e))
    property_data = json.loads(resp.text)
    try:
        item['yearBuilt'] = str(get_dict_value(property_data, ['data', 'property', 'yearBuilt']))
    except:
        item['yearBuilt'] = ''
    try:
        item['address'] = ', '.join(
        [v for v in get_dict_value(property_data, ['data', 'property', 'address']).values() if v])
    except:
        item['address'] = ''
    try:
        item['phone'] = '-'.join(
            get_dict_value(property_data, ['data', 'property', 'contactFormRenderData', 'data', 'contact_recipients'])[
                0]['phone'].values())
    except:
        item['phone'] = ''
    del item['zpid']
    item['ID'] = item["address"]+item["zestimate"]+item[ "rentZestimate"]+item["lotAreaValue"]+item["lotAreaUnit"]+item["lot"]+item["price"]+item["beds"]+item["baths"]+item["sqft"]+item["yearBuilt"]+item["phone"]
    processed.append(item)
    # writer.writerow(item)
    # fileout.flush()
    global items_count
    print(items_count)
    items_count += 1


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


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    Rfile = open('input_zillow.txt', 'r')
    inputfile = Rfile.read()
    links = inputfile.split('\n')
    links = [z for z in links if z.strip()]
    for link in links[:9]:
        link = 'https://www.zillow.com/homes/for_sale/house_type/2-_beds/1.0-_baths/?searchQueryState={"usersSearchTerm":"'+link+'","mapBounds":{"west":-83.17971427663402,"east":-80.22878647520379,"south":39.854585872140056,"north":42.289974185790435},"isMapVisible":true,"filterState":{"beds":{"min":2},"baths":{"min":1},"sort":{"value":"globalrelevanceex"},"ah":{"value":true},"con":{"value":false},"mf":{"value":false},"manu":{"value":false},"land":{"value":false},"tow":{"value":false},"apa":{"value":false},"fsba":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false},"pmf":{"value":false},"pf":{"value":false},"sqft":{"min":1000}},"isListVisible":true,"mapZoom":8,"customRegionId":"d37315ffe2X1-CR1vwsc7pebl56m_u77s3","pagination":{}}'
        # link = f'https://www.zillow.com/homes/{link}_rb/'
        driver.get(link)
        while True:
            #wait for captcha solve
            if 'https://www.zillow.com/captchaPerimeterX/' in driver.current_url:
                driver.quit()
                driver = webdriver.Firefox()
                driver.maximize_window()
                driver.get(link)
                time.sleep(5)
            else:
                break
        while not [v for v in driver.requests if 'https://www.zillow.com/search/GetSearchPageState.htm' in v.url]:
            time.sleep(1)
        data = None
        while not data:
            for req in [v for v in driver.requests if 'https://www.zillow.com/search/GetSearchPageState.htm' in v.url]:
                try:
                    req = [v for v in driver.requests if 'https://www.zillow.com/search/GetSearchPageState.htm' in v.url][0]
                    data = json.loads(req.response.body.decode('utf-8'))
                    break
                except:
                    pass

        items = []
        while True:
            try:
                driver.find_element_by_class_name('list-card-link.list-card-link-top-margin.list-card-img').click()
                time.sleep(10)
                try:
                    if 'There was an error retrieving some ' in driver.find_element_by_css_selector('.zsg-notification-bar > span:nth-child(1)').text:
                        driver.find_element_by_css_selector('.zsg-link').click()
                except:
                    pass
                while True:
                    # wait for captcha solve
                    if 'https://www.zillow.com/captchaPerimeterX/' in driver.current_url:
                        driver.quit()
                        driver = webdriver.Firefox()
                        driver.maximize_window()
                        driver.get(link)
                        time.sleep(5)
                    else:
                        break
                break
            except:
                pass
        while not [v for v in driver.requests if 'https://www.zillow.com/graphql/?zpid' in v.url]:
            driver.get(driver.current_url)
        req_ = [v for v in driver.requests if 'https://www.zillow.com/graphql/?zpid' in v.url][0]
        headers = dict(req_.headers)
        for z_property in get_dict_value(data, ['cat2', 'searchResults', 'mapResults']):
            item = dict()
            try:
                item['address'] = z_property['detailUrl'].split('/')[2].replace('-', ' ')
            except:
                item['address'] = ''
            try:
                item['zestimate'] = str(get_dict_value(z_property, ['hdpData', 'homeInfo', 'zestimate']))
            except:
                item['zestimate'] = ''
            try:
                item['rentZestimate'] = str(get_dict_value(z_property, ['hdpData', 'homeInfo', 'rentZestimate']))
            except:
                item['rentZestimate'] = ''
            try:
                item['lotAreaValue'] = str(get_dict_value(z_property, ['hdpData', 'homeInfo', 'lotAreaValue']))
            except:
                item['lotAreaValue'] = ''
            try:
                item['lotAreaUnit'] = str(get_dict_value(z_property, ['hdpData', 'homeInfo', 'lotAreaUnit']))
            except:
                item['lotAreaUnit'] = ''
            try:
                item['lot'] = str('{} {}'.format(item['lotAreaValue'], item['lotAreaUnit']))
            except:
                item['lot'] = ''
            try:
                item['price'] = str(z_property['price'])
            except:
                item['price'] = ''
            try:
                item['beds'] = str(z_property['beds'])
            except:
                item['beds'] = ''
            try:
                item['baths'] = str(z_property['baths'])
            except:
                item['baths'] = ''
            try:
                item['sqft'] = str(z_property['area'])
            except:
                item['sqft'] = ''
            try:
                item['zpid'] = str(z_property['zpid'])
            except:
                pass
            items.append(item)
        for chunk in chunks(items, 10):
            threads = []
            for item in chunk:
                try:
                    url = f'https://www.zillow.com/graphql/?zpid={item["zpid"]}&contactFormRenderParameter=&queryId=eae0aee8a4d6145e0450075bce43ac72&operationName=ForSaleDoubleScrollFullRenderQuery'
                    req_body = {'operationName': 'ForSaleDoubleScrollFullRenderQuery', 'variables': {'zpid': item['zpid'],'contactFormRenderParameter': {'zpid': item['zpid'],'platform': 'desktop','isDoubleScroll': True}},'clientVersion': 'home-details/6.0.11.0.0.hotfix-01-08-21.8796de6','queryId': 'eae0aee8a4d6145e0450075bce43ac72'}
                except:
                    continue
                # headers = {'Host': 'www.zillow.com', 'Connection': 'keep-alive', 'Content-Length': '285', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'content-type': 'text/plain', 'Accept': '*/*', 'Origin': 'https://www.zillow.com', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://www.zillow.com/homedetails/678-Woodland-St-SW-Hartville-OH-44632/60956688_zpid/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'JSESSIONID=7F83A9A5015106C34E6A1F14A13C92FF; zguid=23|%2467926f66-7c56-42cc-9db2-03eb46689287; zgsession=1|eca62a6a-1472-4613-8059-68b1d3b1bbe7; _ga=GA1.2.1451377432.1610615019; _gid=GA1.2.1096109709.1610615019; zjs_user_id=null; zjs_anonymous_id=%2267926f66-7c56-42cc-9db2-03eb46689287%22; _pxvid=68b7221d-5647-11eb-88c4-0242ac120008; search=6|1613207030398%7Crect%3D43.27887111741266%252C-78.0732689306064%252C38.81238956308905%252C-85.3352318212314%26crid%3Dd37315ffe2X1-CR1vwsc7pebl56m_u77s3%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26baths%3D1.0-%26beds%3D2-%26type%3Dhouse%26lt%3Dfsbo%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26size%3D1000-%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%09%09%09%09%09%09%09; _gcl_au=1.1.589926339.1610615042; KruxPixel=true; DoubleClickSession=true; AWSALB=brs6EzvVXel3OrSly1tDdASA5XiTWPAET44K7BJBMOtdbg4wX6b9TPKPfvgOYTlT0GLdswYuf3lGyTMFRi/O+/sj2rKDRAk53FB4VhvzMpYyfPMCe24HIKLskqHt; AWSALBCORS=brs6EzvVXel3OrSly1tDdASA5XiTWPAET44K7BJBMOtdbg4wX6b9TPKPfvgOYTlT0GLdswYuf3lGyTMFRi/O+/sj2rKDRAk53FB4VhvzMpYyfPMCe24HIKLskqHt; __gads=ID=54099f04f11ac7e1:T=1610615048:S=ALNI_Mbdnsi7KGkpODryBw4WLIAObqIDPw; KruxAddition=true; _pin_unauth=dWlkPU1EWmpPVEExTkRndE1tRTJaUzAwTWpaa0xXRTVORFF0TWpZNU5XWmtNVFptTTJWag; _fbp=fb.1.1610615071776.1001395651; _px3=9303b918c204e3f7f2732c112fd35ecb57281060d07f91471e2c534a22113c72:7a+Oti0lhH3AolZoCzQP33oq43l9iUbtf6r1zIi4IIJzwsloiOJR/3WktsfZlUvkltMCMwyY+n7wsetCgQoX5g==:1000:6dffdXmVUBOLlsclCSyGqRymlty076bAcMFdyexVRwVZ56Mn5yHH/tp6xz8/b9aXHr3zZNiDullrKJBbG+tOFx7ggYIMvHuqFMGiMtIGyxtGQDPFfffGFtmGl9Iwdg+fTuxpAS1wjSsN3dW/ZDxD4d5mH92dwbBGqPVOEXHmkGM=; _gat=1; _uetsid=741c2aa0564711ebbeaecb792e008916; _uetvid=741c9c50564711ebaf312b65f17f07fa'}

                # make_request(url, headers, item)

                t = Thread(target=make_request, args=(url, headers, item,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
    driver.close()
    airtable_client.insert_records(table_name, processed)
