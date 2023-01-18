from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from capcha import main_loop
import time
import csv
import re
from threading import Thread


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def gettiktokdata(link):
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    try:
        driver.get(link)
    except TimeoutException as ex:
        print("Exception has been thrown. Browser timeout")
        driver.quit()
        return
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
            # time.sleep(3)
            item = dict()
            item['url'] = link
            item['userid'] = link.split('/')[-1]
            item['name'] = driver.find_element(By.CSS_SELECTOR, 'h1[data-e2e="user-subtitle"]').text
            item['following'] = driver.find_element(By.CSS_SELECTOR, 'strong[title="Following"]').text
            item['followers'] = driver.find_element(By.CSS_SELECTOR, 'strong[title="Followers"]').text
            item['likes'] = driver.find_element(By.CSS_SELECTOR, 'strong[title="Likes"]').text
            item['description'] = driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-bio"]').text
            try:
                match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', item['description'])
                item['email'] = match.group(0)
            except:
                pass
            writer.writerow(item)
            csvfile.flush()
            print(item['userid'])
            break
        except:
            if driver.find_element(By.XPATH,
                                   '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div').text == 'Verify to continue:':
                continue
            else:
                break
    driver.quit()

if __name__ == '__main__':
    filenames = open('tiktokinputkeyword.txt', 'r').read().split('\n')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    for filename in filenames:
        inputfile = open(f'{filename} - tiktok_urls_list.txt', 'r')
        listofurls = inputfile.read().split('\n')
        csvfile = open(f'{filename} - tiktokacountdetails.csv', 'w', newline='', encoding='utf-8')
        headers = ['url', 'userid', 'name', 'following', 'followers', 'likes', 'description', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for chunk_links in chunks(listofurls, 5):
            thread2 = []
            for link in chunk_links:
                if link == '':
                    continue
                newt = Thread(target=gettiktokdata, args=(link,))
                newt.start()
                thread2.append(newt)
            for newt in thread2:
                newt.join()

        listofurls.clear()