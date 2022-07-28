import csv
import re
import time
from datetime import datetime, timedelta

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

post = []
past = datetime.now() - timedelta(days=30)
headers = ['Name', 'Facebook URL', 'FB_likeCount', 'FB_subscription', 'Number of posts last month', 'Number of video posts last month', 'Number of video views last month', 'Email', 'Has "about" section']
fileout = open('facebookpagesname.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


def do_scroll(driver):
    global postcount
    scroll_pause_time = 5
    scroll = True
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        for res in driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")[-3:]:
            try:
                date = ''.join([v.text for v in res.find_elements_by_css_selector('.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m .buofh1pr .qzhwtbm6.knvmm38d:nth-child(2) a span') if not v.get_attribute('style') and len(v.text) < 20])
                if datetime.strptime(f"{date.split('at')[0]} {datetime.now().year}", "%d %B %Y") < past:
                    scroll = False
                    break
            except:
                pass
        if scroll == False:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    postcount = len(driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0"))
    return driver


def scroll_video(driver):
    global totalview, vcount
    scroll_pause_time = 5
    scroll = True
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        for dir in driver.find_elements_by_css_selector('.hcukyx3x .j83agx80.btwxx1t3.lhclo0ds .rq0escxv.rj1gh0hx.buofh1pr.ni8dbmo4.stjgntxs.l9j0dhe7')[-20:-16]:
            try:
                if 'weeks' in dir.find_element_by_css_selector('.qzhwtbm6.knvmm38d').text:
                    if int(dir.find_element_by_css_selector('.qzhwtbm6.knvmm38d').text.split()[0]) > 4:
                        scroll = False
                        break
                else:
                    pass
            except:
                pass
        if scroll == False:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    for dri in driver.find_elements_by_css_selector('.j83agx80.btwxx1t3.lhclo0ds .rq0escxv.rj1gh0hx.buofh1pr.ni8dbmo4.stjgntxs.l9j0dhe7'):
        try:
            if dri.find_element_by_css_selector('.qzhwtbm6.knvmm38d .bnpdmtie'):
                vcount += 1
                views = dri.find_element_by_css_selector('.qzhwtbm6.knvmm38d .bnpdmtie').text.split()[0]
                view = convert_str_to_number(views)
                totalview += view
        except:
            pass
    return driver


if __name__ == '__main__':
    inputfile = open('facebookname.txt', 'r')
    names = inputfile.read().split('\n')
    paswordinput = open('facebookpasword.txt', 'r')
    fbpas = paswordinput.read().split('\n')
    options = Options()
    options.add_argument('--disable-notifications')
    # options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element_by_id('email').send_keys(fbpas[0])
    driver.find_element_by_id('pass').send_keys(fbpas[1])
    driver.find_element_by_css_selector("button[name='login']").click()
    for name in names:
        postcount = 0
        totalview = 0
        vcount = 0
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
        driver.find_element_by_css_selector('input[type="search"]').send_keys(name, Keys.ENTER)
        time.sleep(5)
        for re in driver.find_elements_by_css_selector('.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.pfnyh3mw.d2edcug0.aahdfvyu.tvmbv18p a'):
            if 'Pages' in re.text:
                re.click()
                time.sleep(2)
                break
        # link = driver.find_element_by_css_selector('div[role="article"] .j83agx80 .hpfvmrgz.g5gj957u.buofh1pr.rj1gh0hx.o8rfisnq .qzhwtbm6.knvmm38d a').get_attribute('href')
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="article"] .j83agx80 .hpfvmrgz.g5gj957u.buofh1pr.rj1gh0hx.o8rfisnq .qzhwtbm6.knvmm38d a'))).get_attribute('href')
        driver.get(link)

        item = dict()
        item['Name'] = name
        item['Facebook URL'] = driver.current_url
        time.sleep(5)
        response = scrapy.Selector(text=driver.page_source)
        try:
            for res in driver.find_element_by_css_selector('.sjgh65i0.cbu4d94t.j83agx80').find_elements_by_css_selector('.j83agx80'):
                if 'people like this' in res.text:
                    item['FB_likeCount'] = res.text.split()[0]
                if 'people follow this' in res.text:
                    item['FB_subscription'] = res.text.split()[0]
        except:
            pass
        try:
            match = re.search(r'[\w\.-]+@[\w\.-]+', ' '.join(response.css('::text').extract()))
            item['Email'] = match.group(0)
        except:
            item['Email'] = ''
        if 'About' in response.css('.a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7.r8blr3vg ::text').extract():
            item['Has "about" section'] = 'True'
        else:
            item['Has "about" section'] = 'No'
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        do_scroll(driver)
        driver.get(f'{link}videos/?ref=page_internal')
        scroll_video(driver)

        try:
            item['Number of posts last month'] = postcount
        except:
            pass
        try:
            item['Number of video posts last month'] = vcount
        except:
            pass
        try:
            item['Number of video views last month'] = totalview
        except:
            pass

        writer.writerow(item)
        fileout.flush()
    driver.close()
