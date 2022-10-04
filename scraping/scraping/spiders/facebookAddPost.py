import time
# import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
import os
import win32com.client
import gmail_email_read

ad_details = {
    'bedrooms': 4,
    'bathrooms': 2,
    'price': 3100,
    'address': 'Ford Rd, Kelowna, BC V1X, Canada',
    'city': 'City Name',
    'desc': 'djkgaf asdlkfhalsdf',
    'pets': 'Neg'
}
def get_data_from_email():
    gmail_email_read.read_email_from_gmail()


if __name__ == '__main__':
    ad_detail = get_data_from_email()
    cwd = os.getcwd()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1880,1300")
    options.add_argument("--disable-notifications")


    driver = webdriver.Chrome(options=options)
    driver.get('https://www.facebook.com/')

    with open(cwd+"Facebook_Accounts_file.txt", 'r', encoding='utf-8') as FAF:
        DATA = FAF.read().split('\n')
    for data in DATA:
        if data == '':
            continue
        replySentList = []
        username = data.split('>')[0]
        password = data.split('>')[1]


    # driver.maximize_window()



        for _chr in username:
            driver.find_element(By.ID, "email").send_keys(_chr)
            time.sleep(0.2)
        time.sleep(2)

        for _chr in password:
            driver.find_element(By.ID, "pass").send_keys(_chr)
            time.sleep(0.2)

        driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//a[contains(@href,"/marketplace")]').click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Create new listing"]').click()
        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, '.nks5qztm:nth-last-child(1) > div > span > div > a[role="link"]').click()
        time.sleep(5)

        images = ["/home/muneeb/Downloads/Python-1.png \n /home/muneeb/Downloads/images.jpeg \n /home/muneeb/Downloads/profile.jpg"]
        driver.find_element(By.CSS_SELECTOR,
                            'div [aria-label="Marketplace"]  label > input[accept="image/*,image/heif,image/heic"]').send_keys(images[0])

    # for img in images:
    #         photo_elem = driver.find_element(By.CSS_SELECTOR, 'div [aria-label="Marketplace"]  label > input[accept="image/*,image/heif,image/heic"]')
    #         if img != images[len(images)-1]:
    #             photo_elem.send_keys(img + os.linesep)
    #             time.sleep(2)
    #         else:
    #             photo_elem.send_keys(img)
    #
    #         p = 1300
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Home for Sale or Rent']").click()
        time.sleep(3)
        driver.find_elements(By.CSS_SELECTOR, '[role="option"]')[0].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Rental type"]').click()
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, '[role="option"]')[1].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Number of bedrooms"] > div > div input').send_keys(ad_details['bedrooms'])
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Number of bathrooms"] > div > div input').send_keys(ad_details['bathrooms'])
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Price per month"] > div > div input').send_keys(ad_details['price'])
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Rental address"] > div > div input').send_keys(ad_details['address'])
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, '[aria-label="10 suggested searches"] > [role="option"]')[0].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Rental description"] > div > div textarea').send_keys(ad_details['desc'])
        if ad_details['pets'] == 'Neg':
            driver.find_element(By.CSS_SELECTOR, '[aria-label="Cat friendly"]').click()
            driver.find_element(By.CSS_SELECTOR, '[aria-label="Dog friendly"]').click()


        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Next"]').click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Publish"]').click()
        time.sleep(7)
    driver.quit()

