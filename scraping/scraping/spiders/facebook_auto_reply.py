import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    AutomatedMessage = '''Thank you for responding to our ad. The landlord has already received over 30 responses and will probably pick a tenant from those applications. I suggest that you register on the website https://www.homefinders.rentals 

and you will start getting notified with rentals BEFORE we post them here, so you won't miss out on any more great listings!  It is FREE to Register !!

With over 1,100 properties, covering 24 cities across BC, HomeFinders has you covered. You can;
-Search our database (for Free)
-Register (for Free) and be notified when a new rental hits the market that matches what you are looking for.
- Hire us to search through 13 different rental websites every day (so you don't have to).
- Hire us to tip you off on rentals BEFORE they hit the market.

Imagine waking up to a NEW list of rentals every day until you find a place!

Check out this information Video https://youtu.be/7x1x0skLRWs

Proud Member of the Better Business Bureau with an A+ rating for the last 17 years.
https://www.bbb.org/.../renta.../homefinders-0037-2417284...



'''

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
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys(AutomatedMessage)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'div[role="textbox"]').send_keys(Keys.ENTER)
        time.sleep(1)



        driver.find_element(By.CSS_SELECTOR,'div[aria-label="Close chat"]').click()
        time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Your profile"]').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'div[data-visualcompletion="ignore-dynamic"][role="listitem"][data-nocookies="true"]').click()

    driver.quit()



