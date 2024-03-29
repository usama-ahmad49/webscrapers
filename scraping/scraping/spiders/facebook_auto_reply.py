import os
import time

import pdfplumber
import pyperclip
import win32com.client
from docx2pdf import convert
from datetime import date
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    today = date.today()
    # cwd =  'E:\\Project\\pricescraperlk\\webscrapers\\webscrapers\\scraping\\scraping\\spiders\\'
    cwd =  'C:\\Users\\corre\\Desktop\\facebookAutomation\\'
    # open document contaning messgage for auto reply
    # we use docx library for this purpose
    try:
        convert(cwd+"Auto response for Facebook Marketplace.docx", cwd + "Auto response for Facebook Marketplace.pdf")
    except:
        pass

    # open file containg facebook account information
    # Informaton in file must be stored in a perticular pattern to avoid any errors
    # all account information must be in following pattern:
    # useremail>password
    # for adding more then one account in file:
    # add an account info in above pattern then press enter one time then add another account info in above pattern

    with pdfplumber.open(cwd+"Auto response for Facebook Marketplace.pdf") as pdf:
        text = pdf.pages[0]
        Bold_text = text.filter(
            lambda obj: (obj["object_type"] == "char" and "Bold" in obj["fontname"])).extract_text().split('\n')

    textpart = text.extract_text()
    for BT in Bold_text:
        textpart = textpart.split(BT)[0] + '*' + BT.strip() + '* ' + textpart.split(BT)[1]

    AutomatedMessage = textpart
    with open(cwd+"Facebook_Accounts_file.txt", 'r', encoding='utf-8') as FAF:
        DATA = FAF.read().split('\n')

    outlook = win32com.client.Dispatch('outlook.application')
      # go to facebook.om login page

    for data in DATA:
        options = Options()
        options.add_argument('--disable-notifications')  # to disable any unwanted notification popups or alerts
        driver = webdriver.Firefox(service_log_path=os.devnull, options=options)  # open browser
        driver.maximize_window()  # maximize window
        driver.get('https://www.facebook.com/')
        if data == '':
            continue
        replySentList = []
        username = data.split('>')[0]
        password = data.split('>')[1]

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'email')))  # wait for browser to load elements that we need to click
        time.sleep(3)

        driver.find_element(By.ID, 'email').send_keys(username)  # enter username
        time.sleep(0.5)
        driver.find_element(By.ID, 'pass').send_keys(password)  # enter password
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()  # clink login button
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
        time.sleep(3)

        driver.get('https://www.facebook.com/marketplace/inbox')  # go to marketplace inbox after logging in
        time.sleep(3)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Collection of Marketplace items"]')))
            driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Collection of Marketplace items"]')
            time.sleep(3)
        except:
            driver.quit()
            continue
        # get all messages from inbox and loop over them one by one to reply to them individually
        while True:
            try:
                if len(driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Collection of Marketplace items"] div[data-visualcompletion="ignore-dynamic"]')) <2:
                    break
            except:
                break
            count = 0
            for messages in driver.find_elements(By.CSS_SELECTOR,'div[aria-label="Collection of Marketplace items"] div[data-visualcompletion="ignore-dynamic"]'):
                try:
                    a = ActionChains(driver)
                    a.move_to_element(messages).perform()
                    time.sleep(1)
                    messages.click()  # open message box
                    time.sleep(3)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"]')))
                    # click text box in message window
                    driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]').click()
                    time.sleep(1)
                    # clear text box in message window to make sure no extra keystrocks sent to user
                    driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]').clear()
                    time.sleep(1)
                    # paste coppied automated message into the text box to be sent
                    pyperclip.copy(AutomatedMessage)
                    ctrlAction = ActionChains(driver)
                    ctrlAction.key_down(Keys.CONTROL)
                    ctrlAction.send_keys("v")
                    ctrlAction.key_up(Keys.CONTROL)
                    ctrlAction.perform()
                    time.sleep(1)
                    # press enter to send message
                    driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]').send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Chat settings"]').click()
                    time.sleep(1)
                    to = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Chat settings"] h1 span').text
                    replySentList.append(to)
                    driver.find_elements(By.CSS_SELECTOR, 'div[role="menu"] div[role="menuitem"]')[-2].click()
                    time.sleep(1)
                    driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Delete chat"]')[-1].click()
                    # now message sent! close the message window
                    try:
                        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Close chat"]').click()
                    except:
                        pass
                    time.sleep(3)
                except:
                    count +=1
                    if count>1:
                        break
            driver.refresh()
            time.sleep(3)
        # click on the profile element to show logout button
        # try:
        #     driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Your profile"]').click()
        # except:
        #     driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Your profile"]').click()
        time.sleep(1)
        # click logout button
        if len(replySentList) != 0:
            mail = outlook.CreateItem(0)
            mail.To = 'jcisnever@gmail.com'
            mail.Subject = f"Today's Report: {today}; for: {username.split('@')[0]}"
            mail.HTMLBody = f"<b>Today's Report Date: {today}<b><br><br><br>{'<br>'.join(replySentList)}<br>"
            mail.Send()
        driver.quit()





    # all accounts served now close browser and end program
    # driver.quit()
