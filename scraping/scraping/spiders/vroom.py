import requests
import scrapy
import json
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv


csvheaders=['make','model','year','price','millage','trim','vin']
file=open('vroom.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(file,fieldnames=csvheaders)
writer.writeheader()

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


def getlnk():
    global respons
    next=1
    url ='https://www.vroom.com/cars'
    driver=webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div/button').click()
    sleep(6)
    resp=([v for v in driver.requests if 'invsearch-v3-prod-ext.aws.vroomapi.com' in v.path])
    json_data = json.loads(resp[0].response.body)
    cars = get_dict_value(json_data,['data','hits','hits'])
    existing = []
    for car in cars:
        item=dict()
        item['make']=car.get('_source').get('make')
        item['model']=car.get('_source').get('model')
        item['year']=car.get('_source').get('year')
        item['price']=car.get('_source').get('listingPrice')
        item['trim']=car.get('_source').get('trim')
        item['millage']=car.get('_source').get('miles')
        item['vin'] = car.get('_source').get('vin')
        existing.append(item['vin'])
        writer.writerow(item)
        file.flush()
    while(next<700):
        if not driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[3]/div/nav/ul/li[9]/button'):
            driver.refresh()
        else:
            driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[3]/div/nav/ul/li[9]/button').click()
            try:
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[3]/div/nav/ul/li[9]/button')))
            except TimeoutException:
                print('timeout')

            # sleep(6)
        respons = [v for v in driver.requests if 'invsearch-v3-prod-ext.aws.vroomapi.com' in v.path]
        next=next+1
    driver.quit()
    for respon in respons[1:]:
        jsonData = json.loads(respon.response.body)
        cars = get_dict_value(jsonData, ['data', 'hits', 'hits'])
        for car in cars:
            item2 = dict()
            item2['make'] = car.get('_source').get('make')
            item2['model'] = car.get('_source').get('model')
            item2['year'] = car.get('_source').get('year')
            item2['price'] = car.get('_source').get('listingPrice')
            item2['trim'] = car.get('_source').get('trim')
            item2['millage'] = car.get('_source').get('miles')
            item2['vin']=car.get('_source').get('vin')
            if item2['vin'] not in existing:
                existing.append(item2['vin'])
                writer.writerow(item2)
                file.flush()




if __name__ == '__main__':
    getlnk()