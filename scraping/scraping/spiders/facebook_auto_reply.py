import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    username = '**********'
    password = '******'

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
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys('Automated message')
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys(Keys.ENTER)
        time.sleep(1)



        driver.find_element(By.CSS_SELECTOR,'div[aria-label="Close chat"]').click()
        time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Your profile"]').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"][role="listitem"][data-nocookies="true"]').click()

    driver.quit()



