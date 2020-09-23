from seleniumwire import webdriver
import json
import csv

import time

csv_header={'name','discription','productImageUrl','collection','price'}
Wfile=open('woolswoth.csv','w',encoding='utf-8',newline='')
writer=csv.DictWriter(Wfile,fieldnames=csv_header)
writer.writeheader()



i=1
while i!=29:
    driver = webdriver.Ie()
    driver.get("https://www.woolworths.com.au/shop/securelogin")
    driver.implicitly_wait(5)
    loginform = driver.find_element_by_id('loginForm')
    user = loginform.find_element_by_id("loginForm-Email")
    user.send_keys("ithelper420@gmail.com")
    pas = loginform.find_element_by_id("loginForm-Password")
    time.sleep(1)
    pas.send_keys("aaaaaa1")
    time.sleep(2)
    pas.submit()
    # button=loginform.find_element_by_css_selector('button[class="primary-legacy m full-width mobile-full-width"]')
    # button.click()
    time.sleep(5)

    url='https://www.woolworths.com.au/shop/browse/lunch-box?pageNumber={}'.format(i)
    driver.get(url)
    i=i+1
    requests_data = [r for r in driver if 'apis/ui/browse/category' in r.path]
    data = json.loads(requests_data[0].response.body)
    for product_data in data.get('Bundles', []):
        product_data = product_data['Products'][0]
        item = dict()
        item['name'] = product_data.get('Name')
        item['discription'] = product_data.get('RichDescription')
        item['productImageUrl'] = product_data.get('LargeImageFile')
        item['collection'] = product_data.get('Source')
        item['price'] = product_data.get('CupString')
        writer.writerow(item)
        Wfile.flush()
        driver.quit()

