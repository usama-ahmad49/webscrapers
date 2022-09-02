import time

import docx
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    usernamefile = open('twitter_pwd.txt', 'r')
    usernamef = usernamefile.read().split('\n')
    driver = webdriver.Chrome()
    driver.get("https://www.twitter.com")
    driver.maximize_window()
    driver.find_element(By.CSS_SELECTOR,'a[data-testid="loginButton"]').click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="session[username_or_email]"]')))
    driver.find_element(By.CSS_SELECTOR,'input[name="session[username_or_email]"]').send_keys(usernamef[0])
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="session[password]"]')))
    driver.find_element(By.CSS_SELECTOR,'input[name="session[password]"]').send_keys(usernamef[1])
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]')))
    driver.find_element(By.CSS_SELECTOR,'div[data-testid="LoginForm_Login_Button"]').click()