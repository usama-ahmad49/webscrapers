import csv
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import scrapy
import datefinder

headers_csv = ["date", "case", "status", "address", "parcel_number", "url"]

fileout = open('cobbcounty_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()

def do_scroll(driver):
    scroll_pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://cobbca.cobbcounty.org/CitizenAccess/Cap/CapHome.aspx?module=Enforce&TabName=Enforce')
    time.sleep(2)
    do_scroll(driver)

    file_ = open('cobbcounty_input.txt', 'r', encoding='utf-8')
    codes = file_.read().split('\n')
    target_date = next(datefinder.find_dates(codes[0])).date()
    codes = codes[1:]
    for code in codes:
        driver.find_element_by_id('ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber').send_keys(code)
        driver.find_element_by_id('ctl00_PlaceHolderMain_generalSearchForm_txtGSNumber_ChildControl0').send_keys('1')
        driver.find_element_by_id('ctl00_PlaceHolderMain_generalSearchForm_txtGSNumber_ChildControl1').send_keys(
            '99999999')
        time.sleep(1)
        driver.find_element_by_id('ctl00_PlaceHolderMain_btnNewSearch').send_keys(Keys.RETURN)
        time.sleep(1)
        stop = False
        items = []
        while not stop:
            response = scrapy.Selector(text=driver.page_source)
            link_no = 1
            for tr in response.css('#ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList tr')[3:4]:
                item = dict()
                item['date'] = ''.join(tr.css('td:nth-child(2) ::text').extract()).strip()
                try:
                    if target_date > next(datefinder.find_dates(item['date'])).date():
                        stop = True
                except:
                    pass
                url = 'https://eddspermits.gwinnettcounty.com{}'.format(
                    tr.css('td:nth-child(3) ::attr(href)').extract_first(''))
                item['url'] = url
                driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
                driver.get(url)
                inner_response = scrapy.Selector(text=driver.page_source)
                item['case'] = inner_response.css('#ctl00_PlaceHolderMain_lblPermitNumber ::Text').extract_first('')
                item['status'] = inner_response.css('#ctl00_PlaceHolderMain_lblRecordStatus ::Text').extract_first('')
                item['address'] = inner_response.css('#tbl_worklocation ::Text').extract_first('')
                item['parcel_number'] = inner_response.css(
                    '#ctl00_PlaceHolderMain_PermitDetailList1_palParceList .ACA_SmLabel.ACA_SmLabel_FontSize ::Text').extract_first(
                    '')
                if item['case'].strip():
                    writer.writerow(item)
                    fileout.flush()
                items.append(item)
                driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

