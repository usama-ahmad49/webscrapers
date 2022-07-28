import json
import logging
import random
import time
from threading import Thread
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def request_url(url, headersMagento, productskulist):
    while True:
        resp = requests.get(url, headers=headersMagento)

        if resp.status_code == 200:
            break
        else:
            time.sleep(5)
    jdata = json.loads(resp.content.decode('utf-8'))
    for data in jdata['items']:
        productskulist.append(data['sku'])
        # if data['sku'].split('-')[-1].replace('.', '1').isdigit() or data['sku'].split('-')[-1] == 'OS':
        #     if '-'.join(data['sku'].split('-')[:-2]) not in productskulist:
        #         productskulist.append('-'.join(data['sku'].split('-')[:-2]))
        # elif data['sku'].split('-').__len__() == 2:
        #     if data['sku'].split('-')[:-1] not in productskulist:
        #         productskulist.append('-'.join(data['sku'].split('-')[:-1]))


def getskusfrommagento():
    productskulist = []
    # file = open('stockx_skus.txt', 'w', encoding='utf-8')
    url = "https://admin.brandrange.com/index.php/rest/V1/integration/admin/token"

    # headers = CaseInsensitiveDict()
    headers = dict()
    headers["Content-Type"] = "application/json"

    data = '{"username":"nauman.pucit", "password":"nauman.pucit@160#"}'

    resp = requests.post(url, headers=headers, data=data)
    token = resp.text.replace('"', '')
    #
    # print(resp.status_code)
    headersMagento = {'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    while True:
        TRS = requests.get('https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=IRC&searchCriteria[filterGroups][0][filters][0][value]=SNEAKERS STOCK | DS&searchCriteria[pageSize]=1&store_id=1,store_code=en', headers=headersMagento)
        if TRS.status_code == 200:
            break
        else:
            time.sleep(5)
    TotalresultsJson = json.loads(TRS.content.decode('utf-8'))
    TotalCount = TotalresultsJson['total_count']
    page = TotalCount / 5000
    if page.is_integer():
        TotalPages = page
    else:
        TotalPages = int(page) + 1
    i = 1
    URLList = []
    cnt = 0
    while i <= TotalPages:
        URLList.append(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=IRC&searchCriteria[filterGroups][0][filters][0][value]=SNEAKERS STOCK | DS&searchCriteria[pageSize]=5000&searchCriteria[currentPage]={i}&store_id=1,store_code=en&fields=items[sku]')
        i += 1
    for url_chunk in chunks(URLList, 5):
        threads_list_2 = []
        cnt += 1
        print(cnt)

        for url in url_chunk:
            if url == '':
                continue
            newthread = Thread(target=request_url, args=(url, headersMagento, productskulist,))
            newthread.start()
            threads_list_2.append(newthread)

        for t in threads_list_2:
            t.join()

        # file.flush()
    return productskulist
    # for sku in productskulist:
    #     file.write(sku + '\n')
    # file.close()


if __name__ == '__main__':
    allSKUS = open('allSKUS.csv','w',newline="", encoding='utf-8')
    headers = ['sku']
    csvwriter = csv.DictWriter(allSKUS,fieldnames=headers)
    csvwriter.writeheader()
    SKULIST = getskusfrommagento()
    for sku in SKULIST:
        item = dict()
        item['sku'] = sku
        csvwriter.writerow(item)

