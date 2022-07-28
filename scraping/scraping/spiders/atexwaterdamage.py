import csv
import time

import requests
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

headers = ['location city', 'location state', 'facebook phone', 'facebook website', 'facebook email', 'facebook address', 'yp phone number', 'yp.com website', 'yp email.com', 'yp address', 'yelp phone', 'yelp website', 'yelp address', 'www.dexknows.com phone', 'www.dexknows.com web', 'www.dexknows.com email', 'www.dexknows.com address', 'www.superpages.com phone', 'www.superpages.com web', 'www.superpages.com email', 'www.superpages.com address']
fileout = open('atexwaterdamage.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


def yellowpages(ST, loc):
    url = f'https://www.yellowpages.com/search?search_terms={ST}&geo_location_terms={loc}'
    resp = requests.get(url=url)
    respon = resp.text
    response = scrapy.Selector(text=respon)
    geturl = 'https://www.yellowpages.com' + response.css('.search-results.organic .result')[0].css('.business-name::attr(href)').extract_first()
    resp = requests.get(url=geturl)
    respon1 = resp.text
    response1 = scrapy.Selector(text=respon1)
    try:
        phone = response1.css('#main-header .contact .phone::text').extract_first()
    except:
        phone = ''
    try:
        website = response1.css('.primary-btn.website-link::attr(href)').extract_first()
    except:
        website = ''
    try:
        email = response1.css('.email-business::attr(href)').extract_first().split(':')[1]
    except:
        email = ''
    try:
        address = ', '.join(response1.css('#main-header .contact .address ::text').extract())
    except:
        address = ''
    item = [phone, website, email, address]
    return item


def yelp(st, loc):
    url = 'https://www.yelp.com/'
    driver = webdriver.Chrome()
    driver.get(url=url)
    driver.find_element_by_id('find_desc').send_keys(st)
    driver.find_element_by_id('dropperText_Mast').clear()
    driver.find_element_by_id('dropperText_Mast').send_keys(loc)
    driver.find_element_by_id('header-search-submit').click()
    time.sleep(7)
    for resp in driver.find_elements_by_css_selector('.undefined.list__09f24__17TsU .container__09f24__21w3G.hoverable__09f24__2nTf3.margin-t3__09f24__5bM2Z.margin-b3__09f24__1DQ9x.padding-t3__09f24__-R_5x.padding-r3__09f24__1pBFG.padding-b3__09f24__1vW6j.padding-l3__09f24__1yCJf.border--top__09f24__1H_WE.border--right__09f24__28idl.border--bottom__09f24__2FjZW.border--left__09f24__33iol.border-color--default__09f24__R1nRO'):
        if st in resp.find_element_by_css_selector('.heading--h4__09f24__2ijYq.alternate__09f24__39r7c').text:
            url = resp.find_element_by_css_selector('a').get_attribute('href')
    driver.get(url=url)
    time.sleep(3)
    res = driver.find_elements_by_css_selector('.css-0.padding-t2__373c0__11Iek.padding-r2__373c0__28zpp.padding-b2__373c0__34gV1.padding-l2__373c0__1Dr82.border--top__373c0__3gXLy.border--right__373c0__1n3Iv.border--bottom__373c0__3qNtD.border--left__373c0__d1B7K.border-radius--regular__373c0__3KbYS.background-color--white__373c0__2uyKj div.css-1vhakgw.border--top__373c0__3gXLy.border-color--default__373c0__3-ifU')
    i = 0
    while i < len(res):
        if '.com' in res[i].text:
            website = res[i].text
        elif 'Get Direction' in res[i].text:
            address = res[i].text
            address = address.split('\n')[1]
        else:
            phone = res[i].text
        i += 1

    item = [phone, website, address]
    driver.close()
    return item


def dexknows(ST, loc):
    url = f'https://www.dexknows.com/search?search_terms={ST}&geo_location_terms={loc}'
    resp = requests.get(url=url)
    respon = resp.text
    response = scrapy.Selector(text=respon)
    geturl = 'https://www.dexknows.com' + response.css('.search-results.organic .result')[0].css('.business-name::attr(href)').extract_first()
    resp = requests.get(url=geturl)
    respon1 = resp.text
    response1 = scrapy.Selector(text=respon1)
    try:
        phone = response1.css('.phone::text').extract_first()
    except:
        phone = ''
    try:
        website = response1.css('.website-link::attr(href)').extract_first()
    except:
        website = ''
    try:
        email = response1.css('.email-business::attr(href)').extract_first().split(':')[1]
    except:
        email = ''
    try:
        address = response1.css('#main-header .contact .address ::text').extract_first()
    except:
        address = ''
    item = [phone, website, email, address]
    return item


def superpages(ST, loc):
    url = f'https://www.superpages.com/search?search_terms={ST}&geo_location_terms={loc}'
    resp = requests.get(url=url)
    respon = resp.text
    response = scrapy.Selector(text=respon)
    geturl = 'https://www.superpages.com' + response.css('.search-results.organic .result')[0].css('.business-name::attr(href)').extract_first()
    resp = requests.get(url=geturl)
    respon1 = resp.text
    response1 = scrapy.Selector(text=respon1)
    try:
        phone = response1.css('.phone::text').extract_first()
    except:
        phone = ''
    try:
        website = response1.css('.website-link::attr(href)').extract_first()
    except:
        website = ''
    try:
        email = response1.css('.email-business::attr(href)').extract_first().split(':')[1]
    except:
        email = ''
    try:
        address = response1.css('#main-header .contact .address ::text').extract_first()
    except:
        address = ''
    item = [phone, website, email, address]
    return item


def facebook(st, loc):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element_by_id('email').send_keys('rixtysoft01@gmail.com')
    driver.find_element_by_id('pass').send_keys('qwerty123uiop')
    time.sleep(2)
    driver.find_element_by_id('u_0_b').click()
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div/label/input')))
    time.sleep(10)
    driver.find_element_by_css_selector('input[type="search"]').send_keys(st + ' ' + loc)
    time.sleep(1)
    driver.find_element_by_css_selector('input[type="search"]').send_keys(Keys.RETURN)
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/h2/span/span/a')))
    time.sleep(10)
    url = driver.find_element_by_css_selector('div[role="feed"] div[role="article"] a').get_attribute('href')
    driver.get(url)
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div')))
    time.sleep(5)
    about = False
    for resp in driver.find_elements_by_css_selector('div[role="tablist"] a[role="tab"]'):
        if 'About' in resp.get_attribute('text'):
            resp.click()
            time.sleep(10)
            about = True
            break

    if about == False:
        driver.find_element_by_css_selector('div[role="tablist"] div[tabindex="1"] div[role="tab"]').click()
        time.sleep(7)
        for res in driver.find_elements_by_css_selector('div[role="menu"] a[role="menuitemradio"]'):
            if 'About' in res.get_attribute('text'):
                res.click()
                time.sleep(10)
                break

    for contact in driver.find_elements_by_css_selector('.db0gmjza.cbu4d94t.j83agx80.cwj9ozl2 .je60u5p8'):
        if 'CONTACT INFO' in contact.find_element_by_css_selector('.hv4rvrfc.dhix69tm').text:
            con = contact.find_elements_by_css_selector('.j83agx80 .j83agx80.cbu4d94t.sj5x9vvc.cxgpxx05')
            if len(con) == 4:
                phone = con[1].text
                website = con[0].text
                email = con[2].text
            if len(con) == 3:
                phone = con[1].text
                website = con[0].text
            if len(con) == 2:
                website = con[0].text

    try:
        address = driver.find_element_by_css_selector('.db0gmjza.cbu4d94t.j83agx80.cwj9ozl2 .qzhwtbm6.knvmm38d').text
    except:
        address = ''
    item = [phone, website, email, address]
    driver.close()
    return item


if __name__ == '__main__':
    fileinput = open('more-input.csv', 'r', encoding='utf-8')
    inputstr = fileinput.read().split('\n')
    for inp in inputstr:
        searchText = inp.split(',')[0].replace('"', '')
        location = inp.split(',')[1] + ', ' + inp.split(',')[2]
        item = dict()
        # facebooklist = facebook(searchText, location)
        yellopagelist = yellowpages(searchText, location)
        yelplist = yelp(searchText, location)
        dexknowslist = dexknows(searchText, location)
        superpageslist = superpages(searchText, location)
        item['location city'] = inp.split(',')[1]
        item['location state'] = inp.split(',')[2]
        # item['facebook phone'] = facebooklist[0]
        # item['facebook website'] = facebooklist[1]
        # item['facebook email'] = facebooklist[3]
        # item['facebook address'] = facebooklist[4]
        item['yp phone number'] = yellopagelist[0]
        item['yp.com website'] = yellopagelist[1]
        item['yp email.com'] = yellopagelist[2]
        item['yp address'] = yellopagelist[3]
        item['yelp phone'] = yelplist[0]
        item['yelp website'] = yelplist[1]
        item['yelp address'] = yelplist[2]
        item['www.dexknows.com phone'] = dexknowslist[0]
        item['www.dexknows.com web'] = dexknowslist[1]
        item['www.dexknows.com email'] = dexknowslist[2]
        item['www.dexknows.com address'] = dexknowslist[3]
        item['www.superpages.com phone'] = superpageslist[0]
        item['www.superpages.com web'] = superpageslist[1]
        item['www.superpages.com email'] = superpageslist[2]
        item['www.superpages.com address'] = superpageslist[3]
        writer.writerow(item)
        fileout.flush()
