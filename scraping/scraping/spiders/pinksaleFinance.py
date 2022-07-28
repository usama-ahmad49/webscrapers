import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread

cwd = os.getcwd()


def browser(link):
    while True:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % random.choice(PROXYs))
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(link)
        try:
            if driver.find_element(By.CSS_SELECTOR,'head > title').text != None:
                 break
        except:
            driver.close()
            time.sleep(3)
    time.sleep(3)
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(1)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(2)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(3)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(4)').click()
        time.sleep(3)
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(5)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(6)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(7)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR,'.is-flex.mt-1.mb-2 div a:nth-child(8)').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass

    driver.quit()
if __name__ == '__main__':
    with open(f'{cwd}/proxy.txt', 'r') as proxy:
        PROXYs = proxy.read().split('\n')
    TotalLenght = len(PROXYs)

    with open('settingspinksale.txt','r') as settings:
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