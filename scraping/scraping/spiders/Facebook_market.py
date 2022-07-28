import csv
import os
import time
import urllib
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def get_driver(fb_username, fb_password):
    filename = "file.csv"

    with open(filename, 'r', newline='', encoding='utf-8') as data:
        readerobj = csv.DictReader(data)
        datalist = []
        for row in readerobj:
            datalist.append(row)
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-notifications')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.facebook.com/")
    driver.maximize_window()
    email = driver.find_element_by_id("email")
    email.send_keys(fb_username)
    password = driver.find_element_by_id("pass")
    password.send_keys(fb_password)
    password.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.get('https://www.facebook.com/marketplace/create/item')
    time.sleep(1)
    try:
        cookies = driver.find_element_by_xpath('//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v lrazzd5p bwm1u5wc"]')
        cookies.click()
    except:
        print('no cookies')
    time.sleep(1)
    for data in datalist:
        images = data['Images'].split(';')
        for src in images:
            urllib.request.urlretrieve(src, 'imagesss.jpg')  # place names here of images
        driver.get('https://www.facebook.com/marketplace/create/item')
        try:
            par = driver.find_element_by_xpath('//span[contains(text(),"Titre")]').find_element_by_xpath('..')
            title = par.find_element_by_tag_name('input')
            par_price = driver.find_element_by_xpath('//span[contains(text(),"Prix")]').find_element_by_xpath('..')
            price = par_price.find_element_by_tag_name('input')
            par_desc = driver.find_element_by_xpath('//span[contains(text(),"Description")]').find_element_by_xpath('..')
            description = par_desc.find_element_by_tag_name('textarea')
            par_tag = driver.find_element_by_xpath('//span[contains(text(),"Tags produits")]').find_element_by_xpath('..')
            tags = par_tag.find_element_by_tag_name('textarea')
            par_sku = driver.find_element_by_xpath('//span[contains(text(),"SKU")]').find_element_by_xpath('..')
            sku = par_sku.find_element_by_tag_name('input')
            par_place = driver.find_element_by_xpath('//span[contains(text(),"Lieu")]').find_element_by_xpath('..')
            place = par_place.find_element_by_tag_name('input')
            image_loc = driver.find_element_by_css_selector('.aahdfvyu.hv4rvrfc.dati1w0a label input[accept="image/*,image/heif,image/heic"]')
            image_loc.send_keys(path + '\imagesss.jpg')
            title.send_keys(data['Title'])
            price.send_keys(data['Prices'])
            category = driver.find_element_by_css_selector('label[aria-label="Catégorie"]')
            category.click()
            selectCategory = driver.find_elements_by_css_selector('.rm0tqlba.emxnvquj.e4wx1xs5 div[data-visualcompletion="ignore-dynamic"]')[1].click()
            State = driver.find_element_by_css_selector('label[aria-label="État"]')
            State.click()
            StateClick = driver.find_elements_by_css_selector('div[role="menuitemradio"]')[0].click()
            description.send_keys(data['Description'])
            listoftags = data['Tags']
            tag = listoftags.split(';')
            for t in tag:
                tags.send_keys(t)
                tags.send_keys(Keys.RETURN)
            sku.send_keys(data['SKU'])
            place.click()
            time.sleep(0.5)
            driver.find_element_by_css_selector('ul#jsc_c_1c[role="listbox"] li').click()
            # place.clear()
            # place.send_keys(data['Place'])
            driver.find_element_by_css_selector('div[aria-label="Publier"][role="button"]').click()

        except:
            time.sleep(1)
            pass
    return driver


if __name__ == '__main__':
    path = os.getcwd()
    input_file = open('facebook_email.txt', 'r')
    file_data = input_file.read().split('\n')
    fb_username = file_data[0]
    fb_password = file_data[1]
    driver = get_driver(fb_username, fb_password)
    driver.quit()
