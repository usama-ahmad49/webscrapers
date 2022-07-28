import csv
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = ['name', 'joined', 'location']
fileout = open('fblostandfoundpetsofcyprus.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
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


def parsedata(driver):
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    for resp in response.css('.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.pfnyh3mw.d2edcug0.ofv0k9yr.cwj9ozl2 .b20td4e0.muag1w35')[-1].css('.ue3kfks5.pw54ja7n.uo3d90p7.l82x9zwi.a8c37x1j'):
        item = dict()
        item['name'] = resp.css('.qzhwtbm6.knvmm38d span')[1].css('::text').extract_first()
        item['joined'] = resp.css('.qzhwtbm6.knvmm38d span')[2].css('::text').extract_first()
        if ('at' not in resp.css('.qzhwtbm6.knvmm38d span')[4].css('::text').extract_first()) or ('university' not in resp.css('.qzhwtbm6.knvmm38d span')[4].css('::text').extract_first()) or ('college' not in resp.css('.qzhwtbm6.knvmm38d span')[4].css('::text').extract_first()):
            item['location'] = resp.css('.qzhwtbm6.knvmm38d span')[4].css('::text').extract_first()
        writer.writerow(item)
        fileout.flush()


if __name__ == '__main__':
    fb_input_file = open('fb_login.txt', 'r')
    fb_input = fb_input_file.read().split('\n')
    fb_input_emial = fb_input[0]
    fb_input_pwd = fb_input[1]
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get('https://www.facebook.com/groups/LostAndFoundPetsOfCyprus/members')
    driver.find_element_by_id('email').send_keys(fb_input_emial)
    driver.find_element_by_id('pass').send_keys(fb_input_pwd)
    driver.find_element_by_id('loginbutton').click()
    time.sleep(10)
    do_scroll(driver)
    parsedata(driver)
    driver.close()
