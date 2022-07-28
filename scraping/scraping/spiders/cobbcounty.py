try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    # driver.switch_to.frame("ACAFrame")
    # driver.find_element_by_id('ctl00_PlaceHolderMain_TabDataList_TabsDataList_ctl00_LinksDataList_ctl01_LinkItemUrl').click()
    # do_scroll(driver)
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
        current_page = '20'
        while not stop:
            while not driver.find_elements_by_id('ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList'):
                try:
                    driver.find_element_by_id('ctl00_PlaceHolderMain_btnNewSearch').send_keys(Keys.RETURN)
                except:
                    pass
                time.sleep(5)
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
                link_no += 1
                try:
                    driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_ctl0{}_hlPermitNumber"]'.format(link_no)).click()
                    time.sleep(1)
                except:
                    continue
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
                driver.back()
                do_scroll(driver)
                if current_page:
                    time.sleep(3)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList"]/tbody/tr[13]/td/table')))
                    while not [v for v in driver.find_elements_by_class_name('aca_pagination_td') if v.text==current_page]:
                        try:
                            [v for v in driver.find_elements_by_class_name('aca_pagination_td') if '...' in v.text][0].click()
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList"]/tbody/tr[13]/td/table')))
                        except:
                            time.sleep(1)
                            pass
                    time.sleep(3)
                    button = [v for v in driver.find_elements_by_class_name('aca_pagination_td') if v.text == current_page][0]
                    button.click()
                    do_scroll(driver)
                time.sleep(1)
            if stop:
                break
            time.sleep(1)

            driver.find_elements_by_class_name('aca_simple_text.font11px')[-1].send_keys(Keys.RETURN)
            time.sleep(5)
            current_page = driver.find_element_by_class_name('SelectedPageButton.font11px').text
            do_scroll(driver)
            while driver.find_elements_by_class_name(
                    'SelectedPageButton.font11px') and str(int(current_page)-1) == driver.find_element_by_class_name(
                    'SelectedPageButton.font11px').text:
                time.sleep(1)
