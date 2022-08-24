import os
import time
import docx
import scrapy
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

if __name__ == '__main__':
    try:
        doc = docx.Document('Auto response for Facebook Marketplace.docx')
        AutomatedMessage = ''
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        AutomatedMessage = '\r'.join(fullText)
    except IOError:
        print('error opening file')
        exit()

    username = 'f.nobel301@gmail.com'
    password = 'Kelowna1!'

    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element(By.ID, 'email').send_keys(username)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
    time.sleep(3)

    driver.get('https://www.facebook.com/marketplace/inbox')
    time.sleep(3)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Collection of Marketplace items"]')))
    driver.find_element(By.CSS_SELECTOR,'div[aria-label="Collection of Marketplace items"]')
    time.sleep(3)
    for messages in driver.find_elements(By.CSS_SELECTOR,'div[aria-label="Collection of Marketplace items"] div[data-visualcompletion="ignore-dynamic"]')[1:]:
        messages.click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').clear()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys(AutomatedMessage.replace('\n','\r'))
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys(Keys.ENTER)
        time.sleep(1)



        driver.find_element(By.CSS_SELECTOR,'div[aria-label="Close chat"]').click()
        time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Your profile"]').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"][role="listitem"][data-nocookies="true"]').click()

    driver.quit()



