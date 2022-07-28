import json
import time
from datetime import date, datetime

import scrapy
from selenium import webdriver

print(str(datetime.now()))
filename = 'bigbetbiz.json'
fileout = open(filename, 'w')
# fileout.write('[' + '\n')
if __name__ == '__main__':
    url = 'https://bigbetbiz.com/'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_css_selector('input[data="txtAccount"]').send_keys('B18133')
    driver.find_element_by_css_selector('input[id="txtPassword"]').send_keys('Jwins1980')
    time.sleep(1)
    driver.find_element_by_class_name('btn-success').click()
    time.sleep(3)
    for selector in driver.find_elements_by_css_selector('#accordion .card.mb-2'):
        selector.find_element_by_css_selector('li:nth-child(2) button').click()
        time.sleep((0.5))
    time.sleep(1)
    driver.find_element_by_css_selector('.card.sticky-top.mb-2 .btn.btn-success.float-right').click()
    time.sleep(5)
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    driver.quit()
    time.sleep(1)
    global date1
    items = []
    for resp in response.css('#accordion .card.container-for-filter.mb-2'):
        for respo in resp.css('.card-body.p-0 div'):
            if respo.css('[date-info]'):
                date1 = respo.css('[date-info] ::attr(date-info)').extract_first()
            elif respo.css('.bet-schedule-section.container-for-filter '):
                newItem = dict()
                for res in respo.css('.bet-schedule-section.container-for-filter'):
                    item = dict()
                    try:
                        item['Game Title'] = resp.css('.card-header.bet-header-background.sticky-top-header-level-2.container-for-filter ::text').extract_first().split('-')[0]
                    except:
                        pass
                    try:
                        item['Game Subcategory'] = resp.css('.card-header.bet-header-background.sticky-top-header-level-2.container-for-filter ::text').extract_first().split('-')[1]
                    except:
                        pass
                    try:
                        item['FirstTeam'] = res.css('.col-6.cl-rpy-2.cl-rpx-2.bet-item-title span:nth-child(3)::text').extract()[0]
                    except:
                        pass
                    try:
                        item['SecondTeam'] = res.css('.col-6.cl-rpy-2.cl-rpx-2.bet-item-title span:nth-child(3)::text').extract()[1]
                    except:
                        pass
                    try:
                        item['Team1spread'] = res.css('.col-2.cl-rpy-2.pl-0 ::text').extract()[0]
                    except:
                        pass
                    try:
                        item['Team2spread'] = res.css('.col-2.cl-rpy-2.pl-0 ::text').extract()[1]
                    except:
                        pass
                    try:
                        item['Team1Total'] = res.css('.col-2.cl-rpy-2.p-0 ::text').extract()[0]
                    except:
                        pass
                    try:
                        item['Team2Total'] = res.css('.col-2.cl-rpy-2.p-0 ::text').extract()[1]
                    except:
                        pass
                    try:
                        item['Team1money'] = res.css('.col-2.cl-rpy-2.pr-0 ::text').extract()[0]
                    except:
                        pass
                    try:
                        item['Team2money'] = res.css('.col-2.cl-rpy-2.pr-0 ::text').extract()[1]
                    except:
                        pass
                    try:
                        item['Time'] = date1.split(',')[1]
                    except:
                        pass
                    try:
                        item['Date'] = date1.split(',')[0]
                    except:
                        pass
                    out_item = dict()
                    out_item['full_match'] = item
                    items.append(out_item)
                    # fileout.write('{"full_match":')
                    # json_object = json.dumps(item, indent=20)
                    # fileout.write(json_object)
                    # fileout.write('},')
                    # fileout.flush()
    items_json_str = json.dumps(items)
    fileout.write(items_json_str)
    # fileout.write(']' + '\n')
    # driver.close()
    print(str(datetime.now()))
