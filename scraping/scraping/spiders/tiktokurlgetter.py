import sys

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from capcha import main_loop
import time
import csv
inputfile = open('tiktokinputkeyword.txt','r')
inputkeyword = inputfile.read().split('\n')

# header_names = ['URL']
# csv_writer = csv.DictWriter(cs, fieldnames=header_names)
# csv_writer.writeheader()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")


for keyword in inputkeyword:
    cs = open(f'{keyword} - tiktok_urls_list.txt', 'w')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(f"https://www.tiktok.com/search/user?q={keyword}")
    time.sleep(5)
    all_profile_urls = []
    while True:
        try:
            if driver.find_element(By.XPATH,
                                   '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                location = driver.find_element(By.CSS_SELECTOR, '#tiktok-verify-ele div[role="dialog"]').location
                size = driver.find_element(By.CSS_SELECTOR, '#tiktok-verify-ele div[role="dialog"]').size
                while True:
                    try:
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[2]/img[2]')))
                        try:
                            distance2 = main_loop(location=location,size=size)

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
            for loop in driver.find_elements(By.CSS_SELECTOR, 'div.tiktok-1fwlm1o-DivPanelContainer.ea3pfar2 > div'):
                try:
                    profile_url = loop.find_element(By.CSS_SELECTOR, 'a[data-e2e="search-user-avatar"]').get_attribute('href')
                    if profile_url not in all_profile_urls:
                        cs.write(profile_url + '\n')
                        # item = dict()
                        # item['URL'] = profile_url
                        # csv_writer.writerow(item)
                        cs.flush()
                        all_profile_urls.append(profile_url)
                except:
                    continue


            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e="search-load-more"]')))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="search-load-more"]').click()
            except:
                try:
                    if driver.find_element(By.XPATH,
                                       '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                        continue
                except:
                    break


        except:
            try:
                if driver.find_element(By.XPATH,
                                       '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                    continue
            except:
                break

        # time.sleep(5)
    cs.close()
    driver.quit()