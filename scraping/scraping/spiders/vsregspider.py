import csv
import time

import scrapy
from selenium import webdriver

headers = ['companyid', 'branch_total', 'branch_code', 'vname', 'vaddress', 'vzip', 'vdate']
fileout = open('vsregspider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


def parsedata():
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    for resp in response.css('div table tbody tr')[2:-2]:
        item = dict()
        item['companyid'] = response.css('div > b > font > b > font::text').extract_first().strip()
        item['branch_total'] = response.css('div table tbody tr')[-1].css('td ::text').extract()[1]
        item['branch_code'] = resp.css('td:nth-child(3) ::text').extract_first().strip()
        item['vname'] = resp.css('td:nth-child(4) ::text').extract_first().strip()
        item['vaddress'] = resp.css('td:nth-child(5) ::text').extract_first().strip()
        item['vzip'] = resp.css('td:nth-child(6) ::text').extract_first().strip()
        item['vdate'] = resp.css('td:nth-child(7) ::text').extract_first().strip()
        writer.writerow(item)
        fileout.flush()


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://vsreg.rd.go.th/VATINFOWSWeb/jsp/V001.jsp')
    time.sleep(3)
    fileinput = open('input.txt', 'r')
    inp = fileinput.read().split()
    for compid in inp:
        driver.find_element_by_id('txtTin').send_keys(compid)
        driver.find_element_by_id('btnSearch').click()
        try:
            t_pg = int(driver.find_elements_by_css_selector('body > div > table > tbody > tr')[-1].find_element_by_css_selector('td > table > tbody > tr > td:nth-child(1) > font:nth-child(2)').text)
        except:
            t_pg = 0
        parsedata()
        j = 0
        while j < t_pg:
            try:
                if 'ย้อนกลับ' in driver.find_elements_by_css_selector('div > table > tbody > tr')[-1].find_elements_by_css_selector('td > table > tbody > tr > td:nth-child(2) > span')[0].text:
                    i = 1
                    t_SP = 6
                else:
                    i = 0
                    t_SP = 5
                if 'ถัดไป' not in driver.find_elements_by_css_selector('div > table > tbody > tr')[-1].find_elements_by_css_selector('td > table > tbody > tr > td:nth-child(2) > span')[-1].text:
                    i = 1
                    t_SP = 5
                j += 5
                while i < t_SP:
                    driver.find_elements_by_css_selector('div > table > tbody > tr')[-1].find_elements_by_css_selector('td > table > tbody > tr > td:nth-child(2) > span')[i].click()
                    i += 1
                    parsedata()
            except:
                j += 5
                pass
    driver.close()
