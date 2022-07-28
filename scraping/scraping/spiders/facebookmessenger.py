try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import time
from os import listdir
import os
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    fileusename = open('usernameFacebook.txt', 'r')
    infileusername = fileusename.read().split('\n')

    usernamelistFile = open('listofcontacts.txt', 'r')
    usersList = usernamelistFile.read().split('\n')

    path = os.getcwd ()
    onlyfiles = [f for f in listdir(path+"\\Photos") if isfile(join(path+"\\Photos", f)) and '.jpg' in f]
    onlytextfile = open('textmessagefile.txt','r')
    onlytext = onlytextfile.read()

    # user_name = os.environ.get('USER')
    # password = os.environ.get('password')
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.messenger.com/')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    time.sleep(2)
    driver.execute_script ( "window.scrollTo(0, document.body.scrollHeight);" )
    driver.find_element_by_id('email').send_keys(infileusername[0])
    time.sleep(.5)
    driver.find_element_by_id('pass').send_keys(infileusername[1])
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'loginbutton')))
    time.sleep ( .5 )
    driver.find_element_by_id('loginbutton').click()
    try:
        time.sleep(4)
        driver.find_element_by_css_selector('div[role="dialog"] div[aria-label="Done"]').click()
    except:
        pass
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="New message"]')))
    while True:
        selection = input("\npress 1 to send just text\n"
              "Press 2 to send just picture(s)\n"
              "Press 3 to send both ==> ")
        selection = int(selection)
        if selection in range(1,4):
            break
    for name in usersList:
        if name =='':
            continue
        driver.find_element_by_css_selector('a[aria-label="New message"]').click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Send message to"]')))
        driver.find_element_by_css_selector('input[aria-label="Send message to"]').send_keys(name)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="listbox"] a[role="presentation"]')))
        driver.find_element_by_css_selector('ul[role="listbox"] a[role="presentation"]').click()
        time.sleep(1)
        if selection ==2:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tkr6xdv7 input[accept="image/*,image/heif,image/heic,video/*"]')))
            element = driver.find_element_by_css_selector('div.tkr6xdv7 input[accept="image/*,image/heif,image/heic,video/*"]')
            for file in onlyfiles:
                element.send_keys(path+f"\\Photos\\{file}")
                time.sleep(3)
            driver.find_element_by_css_selector ( 'div[aria-label="Press Enter to send"]' ).click ()
        elif selection == 1:
            driver.find_element_by_css_selector('div[aria-label="Message"]').send_keys(onlytext)
            driver.find_element_by_css_selector ( 'div[aria-label="Press Enter to send"]' ).click ()
        elif selection == 3:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tkr6xdv7 input[accept="image/*,image/heif,image/heic,video/*"]')))
            element = driver.find_element_by_css_selector('div.tkr6xdv7 input[accept="image/*,image/heif,image/heic,video/*"]')
            for file in onlyfiles:
                element.send_keys(f"C:\\Users\\user\\Desktop\\{file}")
                time.sleep(3)

            driver.find_element_by_css_selector('div[aria-label="Message"]').send_keys(onlytext)
            time.sleep(2)
            driver.find_element_by_css_selector ( 'div[aria-label="Press Enter to send"]' ).click ()
    driver.quit()
    print('system run complete...')