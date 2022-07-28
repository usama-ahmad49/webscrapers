import os
import random
import time

from selenium import webdriver
from threading import Thread

cwd = os.getcwd()


def browser(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % random.choice(PROXYs))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(link)
    try:
        try:
            driver.find_element_by_css_selector('.component-host-scrollable .modal-header button.close').click()
        except:
            pass
        time.sleep(2)
        count = 0
        while True:
            try:
                count+=1
                driver.find_element_by_css_selector('.favs-button.ng-tns-c162-2.ng-star-inserted').click()
                break
            except:
                time.sleep(0.25)
                if count>20:
                    break
        time.sleep(2)
        count = 0
        while True:
            try:
                count+=1
                driver.find_element_by_css_selector('.shared-button.ng-tns-c162-2.ng-star-inserted').click()
                break
            except:
                time.sleep(0.25)
                if count > 20:
                    break
        time.sleep(2)
        count = 0
        while True:
            try:
                count += 1
                driver.find_element_by_css_selector('a.btn-twitter').click()
                break
            except:
                time.sleep(0.25)
                if count > 20:
                    break
        time.sleep(2)
        count = 0
        while True:
            try:
                count += 1
                driver.find_element_by_css_selector('button.close.ng-star-inserted').click()
                break
            except:
                time.sleep(0.25)
                if count > 20:
                    break
        driver.close()
    except:
        pass
if __name__ == '__main__':
    with open(f'{cwd}/proxy.txt', 'r') as proxy:
        PROXYs = proxy.read().split('\n')
    TotalLenght = len(PROXYs)

    with open('settings.txt','r') as settings:
        set = settings.read().split('\n')
        url = set[0]
        threads = int(set[1])
        repeat = set[-1]

    while True:
        threads_list = []
        for i in range(0,threads):
            newt = Thread(target=browser, args=(url,))
            newt.start()
            threads_list.append(newt)
        for t in threads_list:
            t.join()
        if repeat == 'yes':
            time.sleep(10)
        elif repeat == 'no':
            break