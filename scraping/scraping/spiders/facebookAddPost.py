import time
# import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
import os
import win32com.client
import gmail_email_read




if __name__ == '__main__':
    imagefoldername = r"E:\Project\pricescraperlk\webscrapers\webscrapers\scraping\scraping\spiders\attachment"
    ad_detail = gmail_email_read.read_email_from_gmail()
    options = webdriver.FirefoxOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1880,1300")
    options.add_argument("--disable-notifications")


    driver = webdriver.Firefox(options=options)
    driver.get('https://www.facebook.com/')
    for Data in ad_detail:
        usernamePassword = Data['account'].split('>')
        username = usernamePassword[0]
        password = usernamePassword[1]
        driver.maximize_window()

        for _chr in username:
            driver.find_element(By.ID, "email").send_keys(_chr)
            time.sleep(0.2)
        time.sleep(2)

        for _chr in password:
            driver.find_element(By.ID, "pass").send_keys(_chr)
            time.sleep(0.2)

        driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()
        time.sleep(3)
        driver.get('https://www.facebook.com/marketplace/create/rental')
        time.sleep(5)
        # driver.find_element(By.XPATH, '//a[contains(@href,"/marketplace")]').click()
        # time.sleep(3)
        # driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Create new listing"]').click()
        # driver.implicitly_wait(5)
        # driver.find_element(By.CSS_SELECTOR, '.nks5qztm:nth-last-child(1) > div > span > div > a[role="link"]').click()
        # time.sleep(5)
        images = []
        for image in Data['image']:
            images.append(imagefoldername+image+'.jpg')
        # for image in images:
        #     driver.find_element(By.CSS_SELECTOR,'a[aria-label="Add Photos"] input[name="photos-input"]').send_keys(image)

        for img in images:
            photo_elem = driver.find_element(By.CSS_SELECTOR, 'input[accept="image/*,image/heif,image/heic"]')
            if img != images[len(images)-1]:
                photo_elem.send_keys(img + os.linesep)
                time.sleep(2)
            else:
                photo_elem.send_keys(img)

            p = 1300
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Home for Sale or Rent"]').click()
        time.sleep(3)
        driver.find_elements(By.CSS_SELECTOR, '[role="option"]')[0].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Rental type"]').click()
        time.sleep(2)
        propertyType = Data['Property Type']
        if 'House' in Data['Property Type']:
            driver.find_elements(By.CSS_SELECTOR, 'div[role="option"]')[1].click()
        elif 'Apartment' in Data['Property Type']:
            driver.find_elements(By.CSS_SELECTOR, 'div[role="option"]')[0].click()
        elif 'Townhouse' in Data['Property Type']:
            driver.find_elements(By.CSS_SELECTOR, 'div[role="option"]')[2].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Number of bedrooms"] > div > div input').send_keys((int(Data['Bedrooms'].strip())))
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Number of bathrooms"] > div > div input').send_keys((int(Data['Bedrooms'].strip())))
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Price per month"] > div > div input').send_keys(Data['Price'].strip())
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Rental address"] > div > div input').send_keys(Data['Address'].strip())
        time.sleep(3)
        driver.find_elements(By.CSS_SELECTOR, 'ul[aria-label="10 suggested searches"] > li[role="option"]')[0].click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Rental description"] > div > div textarea').send_keys(Data['Description'])
        pets = Data['Pets'].split('\r')[0].strip()
        if pets != 'No':
            driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Cat friendly"]').click()
            driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Dog friendly"]').click()


        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Next"]').click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Publish"]').click()
        time.sleep(7)

        for img in images:
            os.remove(img)

    driver.quit()

