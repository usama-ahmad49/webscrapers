try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import datetime
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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


def do_task(driver, url, size, cvv):
    driver.get(url)
    try:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        driver.find_element_by_id('nav-cart').click()
        time.sleep(5)
        while True:
            if len(driver.find_elements_by_xpath("//button[text()='Remove']")) != 0:
                for e in driver.find_elements_by_css_selector('ul li button[name="remove-item-button"]'):
                    try:
                        e.click()
                        time.sleep(5)
                    except:
                        pass
            else:
                break
            driver.refresh()
            time.sleep(3)
    except:
        pass
    driver.get(url)
    while not driver.current_url == url:
        driver.get(url)
        time.sleep(3)
    e = None
    # try:
    #     actions.move_to_element(driver.find_element_by_xpath('//label[text()="{}"]'.format(size))).perform()
    #     driver.get(url)
    #     time.sleep(5)
    #     e = 1
    # except:
    #     pass
    try:
        driver.find_element_by_xpath("//label[text()='{}']".format(size)).click()
    except:
        return
    driver.find_element_by_class_name('ncss-btn-primary-dark.btn-lg.css-y0myut.add-to-cart-btn').click()
    time.sleep(5)
    driver.find_element_by_id('nav-cart').click()
    time.sleep(5)
    driver.find_element_by_class_name('css-1lkcnio.e16pwdtm0').click()
    time.sleep(5)
    do_scroll(driver)
    driver.switch_to.frame(driver.find_element_by_class_name('credit-card-iframe-cvv.mt1.u-full-width'))
    time.sleep(2)
    driver.find_element_by_id('cvNumber').send_keys(cvv)
    driver.switch_to.parent_frame()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="payment"]/div/div[1]/div[2]/div[5]/button').click()
    time.sleep(3)
    do_scroll(driver)

    got = False
    while not got:
        try:
            driver.find_element_by_xpath('//*[@id="orderreview"]/div/div/div/div/section[2]/div/button').click()
            got = True
        except:
            time.sleep(1)
    time.sleep(10)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    return


if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.nike.com/')
    try:
        driver.find_element_by_xpath("//p[text()='United States']").click()
        time.sleep(2)
    except:
        pass
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)
    driver.find_element_by_xpath(
        '//*[@id="gen-nav-commerce-header-v2"]/div[3]/div[1]/div/div/div[3]/div/button').click()
    time.sleep(2)
    driver.find_element_by_name('emailAddress').send_keys('Bigbusiness204@gmail.com')
    driver.find_element_by_name('password').send_keys('Birdman204!')
    'value="SIGN IN"'
    driver.find_element_by_xpath('//input[@value="SIGN IN"]').click()
    time.sleep(2)

    actions = ActionChains(driver)
    while True:
        google_sheet_link = (
            'https://docs.google.com/spreadsheets/d/16kAHQUnfhPLTtD-ezaDpSAJk6-f0uSgvnlnJKGDLMNM/export?format=csv&id=16kAHQUnfhPLTtD-ezaDpSAJk6-f0uSgvnlnJKGDLMNM&gid=0')
        resp = requests.get(google_sheet_link)
        rows = [v.strip() for v in resp.content.decode('utf-8').split('\n')]
        cvv = rows[0].split(',')[3]
        for row in rows:
            url = row.split(',')[0]
            size = row.split(',')[1]
            time_to_order = row.split(',')[2]
            time_now = ':'.join(str(datetime.datetime.now()).split('.')[0].split(':')[:-1]).split()
            if time_now[1][0] == '0':
                time_now = time_now[0] + ' ' + time_now[1][1:]
            else:
                time_now = time_now[0] + ' ' + time_now[1]
            print('{} {}'.format(time_now, time_to_order))

            if time_now == time_to_order:
                # if True:
                got = False
                while not got:
                    try:
                        do_task(driver, url, size, cvv)
                        got = True
                    except Exception as e:
                        print(str(e))
        time.sleep(15)
