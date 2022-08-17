import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    with open('facebookpasword.txt','r',encoding = 'utf-8') as userpwdfile:
        userpass = userpwdfile.read()
        username = userpass.split('\n')[0].strip()
        password = userpass.split('\n')[1].strip()
    with open('Keywordsfile.txt','r',encoding='utf-8') as keywordsfile:
        Keywords = keywordsfile.read().split('\n')
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element(By.ID,'email').send_keys(username)
    driver.find_element(By.ID,'pass').send_keys(password)
    driver.find_element(By.CSS_SELECTOR,"button[name='login']").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
    time.sleep(3)

    for keyword in Keywords:
        driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search Facebook"]').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').clear()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').send_keys(keyword)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').send_keys(Keys.ENTER)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))



