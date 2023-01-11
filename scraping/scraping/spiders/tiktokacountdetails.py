from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from capcha import main_loop
import time
import csv
import re

inputfile = open('tiktok_urls_list.txt', 'r')
listofurls = inputfile.read().split('\n')

csvfile = open('tiktokacountdetails.csv','w',newline = '', encoding='utf-8')
headers = ['url', 'userid','name','following','followers','likes','description','email']
writer = csv.DictWriter(csvfile,fieldnames=headers)
writer.writeheader()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.maximize_window()


for url in listofurls:
    driver.get(url)
    while True:
        try:
            if driver.find_element(By.XPATH,
                                   '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                while True:
                    try:
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[2]/img[2]')))
                        try:
                            distance2 = main_loop()

                        except:
                            distance2 = 10

                        dragable = driver.find_element(By.XPATH, '//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
                        quoitent = int(distance2 / 20)
                        remainder = distance2 % 20
                        hit = ActionChains(driver).click_and_hold(dragable)
                        for i in range(1, quoitent + 2):
                            if i == quoitent + 1:
                                hit.move_by_offset(remainder, 0).release().perform()
                            else:
                                hit.move_by_offset(20, 0)
                        time.sleep(4)
                        try:
                            if driver.find_element(By.XPATH,
                                                   '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                                pass
                        except:
                            break

                    except:
                        pass
        except:
            pass

        try:
            time.sleep(3)
            item = dict()
            item['url'] = url
            item['userid'] = url.split('/')[-1]
            item['name'] = driver.find_element(By.CSS_SELECTOR,'h1[data-e2e="user-subtitle"]').text
            item['following'] = driver.find_element(By.CSS_SELECTOR,'strong[title="Following"]').text
            item['followers'] = driver.find_element(By.CSS_SELECTOR,'strong[title="Followers"]').text
            item['likes'] = driver.find_element(By.CSS_SELECTOR,'strong[title="Likes"]').text
            item['description'] = driver.find_element(By.CSS_SELECTOR,'h2[data-e2e="user-bio"]').text
            try:
                match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', item['description'])
                item['email'] = match.group(0)
            except:
                pass
            writer.writerow(item)
            csvfile.flush()
            break
        except:
            pass