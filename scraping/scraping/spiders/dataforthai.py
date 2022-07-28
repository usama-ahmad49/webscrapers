import csv
import time

import pandas as pd
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

headers = ['company_id', 'name_th', 'name_en', 'industry_code', 'industry_name', 'objective', 'status', 'registered', 'capital2',
           'address', 'website', 'phone', 'email', 'director_total', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
           'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19', 'd20',
           'signing_conditions', 'report_year', 'fp0', 'fp1', 'fp2', 'fp3', 'fp4', 'fp5', 'fp6',
           'fp7', 'fp8', 'fp9', 'fp10', 'fp11', 'fp12', 'fp13', 'revenue_main', 'revenue_total', 'cgs', 'sga',
           'expense_total', 'interest', 'profit_before_tax', 'tax', 'profit']
fileinput = open('dataforthai.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileinput, fieldnames=headers)
writer.writeheader()


def driverget(url):
    got = True
    while got:
        try:
            driver.get(url=url)
            return driver
        except TimeoutException as e:
            print(e)
            print('try reloading...')


def parse(url, ind_code):
    got = True
    while got:
        try:
            driver.get(url)
            got = False
        except:
            print('try reloading...')
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    for resp in response.css('#datatable tbody tr'):
        url = 'https://www.dataforthai.com' + resp.css('td a::attr(href)').extract_first()
        try:
            parse2(url, ind_code)
        except:
            pass


def parse2(url, ind_code):
    got = True
    while got:
        try:
            driver.get(url)
            got = False
        except:
            print('try reloading...')
    time.sleep(3)
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    item = dict()
    item['company_id'] = response.css('#main_data table td table:nth-child(1) tr td::text').extract()[1]
    item['name_th'] = response.css('#main_data h2::text').extract_first()
    item['name_en'] = response.css('#main_data h3::text').extract_first()
    item['industry_code'] = ind_code
    item['industry_name'] = response.css('#main_data table td table:nth-child(2) tr td::text').extract()[1]
    if len(response.css('#main_data table td table:nth-child(2) tr td::text').extract()) == 4:
        item['objective'] = response.css('#main_data table td table:nth-child(2) tr td::text').extract()[2]
    item['status'] = response.css('#main_data table td table:nth-child(3) tr td::text').extract()[1]
    item['registered'] = response.css('#main_data table td table:nth-child(4) tr td::text').extract()[1]
    item['capital2'] = response.css('#main_data table td table:nth-child(5) tr td::text').extract()[1]
    item['address'] = response.css('#main_data table td table:nth-child(6) tr td a::text').extract_first()
    try:
        for respo in response.css(
                'div.visible-xs.hidden-sm.hidden-md.hidden-lg.notprint > table:nth-child(3) > tbody > tr > td > table'):
            if respo.css('tbody > tr:nth-child(1) > td ::text').extract_first().split()[0] == 'จำนวนกรรมการ':
                item['director_total'] = respo.css('tbody > tr:nth-child(1) > td ::Text').extract_first().split()[1]
                for i, dir in enumerate(respo.css(' tbody > tr')[1:]):
                    item[f'd{i + 1}'] = dir.css('td:nth-child(2)::text').extract_first('').split('. ')[1]
                    if i >= 20:
                        break
        for ress in response.css(
                'div.visible-xs.hidden-sm.hidden-md.hidden-lg.notprint > table:nth-child(3) > tbody > tr > td > table'):
            if ress.css('tbody > tr:nth-child(1) > td ::text').extract_first() == 'กรรมการที่ลงชื่อผูกพันได้':
                item['signing_conditions'] = ' '.join(ress.css('tr')[1:].css('td ::text').extract())
                break
    except:
        pass
    for respd in response.css('table[style="width:100%;border:0px solid;background:#DAF7A6;"]')[:3]:
        if len(respd.css('td ::text').extract()) > 1:
            if '@' in respd.css('td ::text').extract()[1]:
                item['email'] = respd.css('td ::text').extract()[1]
            if (respd.css('td ::text').extract()[1]).strip().isdigit():
                item['phone'] = respd.css('td ::text').extract()[1].strip()
    try:
        item['website'] = response.css('table[style="width:100%;border:0px solid;background:#FFE6DA;"]')[1].css(
            'tr:nth-child(2) a::text').extract_first()
    except:
        pass
    # try :
    #     if '@' in response.css ( 'table[style="width:100%;border:0px solid;background:#DAF7A6;"]' )[-2].css ('td:nth-child(2) ::text' ).extract_first ():
    #         item['email'] = response.css ( 'table[style="width:100%;border:0px solid;background:#DAF7A6;"]' )[-2].css (
    #             'td:nth-child(2) ::text' ).extract_first ()
    #     if response.css ( 'table[style="width:100%;border:0px solid;background:#DAF7A6;"]' )[-2].css ('td:nth-child(2) ::text' ).extract_first ().isdigit():
    #         item['phone'] = response.css('table[style="width:100%;border:0px solid;background:#DAF7A6;"]')[-2].css(
    #             'td:nth-child(2) ::text').extract_first()
    # except :
    #     pass
    # try :
    #     if '@' not in response.css ( 'table[style="width:100%;border:0px solid;background:#DAF7A6;"]' )[-2].css (
    #             'td:nth-child(2) ::text' ).extract_first () :
    #         item['phone'] = response.css ( 'table[style="width:100%;border:0px solid;background:#DAF7A6;"]' )[-2].css (
    #             'td:nth-child(2) ::text' ).extract_first ()
    #     else:
    #         item['phone'] = response.css (
    #         'table[style="width:100%;border:0px solid;background:#bdf160;"] td:nth-child(2) ::text' ).extract_first ('')
    # except :
    #     pass
    # if 'Website' in response.css ( '#main_data table td table:nth-child(7) tr td ::text' ).extract_first () :
    #     item['website'] = response.css (
    #         '#main_data table td table:nth-child(7) table tr td a ::text' ).extract_first ( '' )
    #     try :
    #         item['phone'] = response.css ( '#main_data table td table:nth-child(8) tr td ::text' ).extract ()[1]
    #     except :
    #         pass
    #     try :
    #         item['email'] = response.css ( '#main_data table td table:nth-child(9) tr td ::text' ).extract ()[1]
    #     except :
    #         pass
    # elif 'email' in response.css ( '#main_data table td table:nth-child(7) tr td ::text' ).extract_first () :
    #     item['email'] = response.css ( '#main_data table td table:nth-child(7) tr td ::text' ).extract ()[1]
    # elif 'โทร' in response.css ( '#main_data table td table:nth-child(7) tr td ::text' ).extract_first () :
    #     try :
    #         item['phone'] = response.css ( '#main_data table td table:nth-child(7) tr td ::text' ).extract ()[1]
    #     except :
    #         pass
    #     try :
    #         item['email'] = response.css ( '#main_data table td table:nth-child(8) tr td ::text' ).extract ()[1]
    #     except :
    #         pass
    try:
        driver.find_element_by_css_selector('#main_data table.notprint .pointer').click()
        time.sleep(1)
        ps = driver.page_source
        response = scrapy.Selector(text=ps)
        item['report_year'] = response.css('#fin-desk table th ::text').extract()[1]
        cntr = 1
        for i, res in enumerate(response.css('#fin-desk table tbody:nth-child(2) tr')):
            if res.css('th').__len__() != 0:
                cntr = i
                break
            if res.css('td:nth-child(2)::text').extract_first('').replace('\n', '') != '':
                item[f'fp{i}'] = res.css('td:nth-child(2)::text').extract_first('').replace('\n', '')

        item['revenue_main'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 1].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['revenue_total'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 2].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['cgs'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 4].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['sga'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 5].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['expense_total'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 6].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['interest'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 7].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['profit_before_tax'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 8].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['tax'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 9].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
        item['profit'] = response.css('#fin-desk table tbody:nth-child(2) tr')[cntr + 11].css(
            'td:nth-child(2)::text').extract_first('').replace('\n', '')
    except NoSuchElementException:
        print('no revenue data')
    writer.writerow(item)
    fileinput.flush()


if __name__ == '__main__':
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    got = True
    while got:
        try:
            driver.get('https://www.dataforthai.com/login')
            got = False
        except:
            print('try reloading...')
    driver.find_element_by_id('login-username').send_keys('peterpan345@gmail.com')
    driver.find_element_by_id('login-password').send_keys('345345345')
    driver.find_element_by_id('btn-login').click()
    time.sleep(5)
    driver.find_element_by_id('UpdateBtn').click()
    time.sleep(5)
    df = pd.read_excel('dft list.xlsx', 'Sheet1')
    for weblink in df['IndustryCodeURL']:
        industry_code = weblink.split('/')[-1]
        got = True
        while got:
            try:
                driver.get(weblink)
                got = False
            except:
                print('try reloading...')
        pages = len(driver.find_elements_by_css_selector('.pagination li')[1:-1])
        i = 1
        while i <= int(pages):
            url = weblink + f'/{i}'
            i += 1
            parse(url, industry_code)
    driver.close()
