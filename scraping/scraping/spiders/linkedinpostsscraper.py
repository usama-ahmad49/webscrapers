import ssl
from datetime import date
import time
import smtplib
from email.mime.text import MIMEText

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def email():
    with open('email_crediantials.txt','r',encoding='utf-8') as email:
        crediantials = email.read().split(',')
        sender_email = crediantials[0].split(':')[-1]
        receiver_email = crediantials[1].split(':')[-1]
        password = crediantials[2].split(':')[-1]
    with open('postUrlTosend.txt','r',encoding='utf-8') as file:
        message = file.read()
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = sender_email
    password = password

    # Create a secure SSL context
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here

        sender_email = sender_email
        receiver_email = receiver_email
        message = f"""\
Subject: Linked Post Url {today}

This message is sent from Python App.
{message}"""

        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

if __name__ == '__main__':
    today = date.today()
    fileoutput = open('postUrlTosend.txt','w',encoding='utf-8')
    fileinput = open('linkedin_keywords.txt','r',encoding='utf-8')
    keywords = fileinput.read().split('\n')
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.linkedin.com/login')
    time.sleep(1)
    with open('linkedIn_crediantials.txt','r') as linkedin_crediantials:
        L_C = linkedin_crediantials.read().split(',')
        user_name = L_C[0].split(':')[1]
        password_LI = L_C[1].split(':')[1]
    driver.find_element(By.ID, 'username').send_keys(user_name)
    time.sleep(1)
    driver.find_element(By.ID, 'password').send_keys(password_LI)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sign in"]').click()
    time.sleep(5)
    postUrl = []
    for i,keyword in enumerate(keywords):
        if keyword == '':
            continue
        search_element = driver.find_element(By.CSS_SELECTOR,'#global-nav-typeahead > input')
        actions = ActionChains(driver)
        actions.move_to_element(search_element).perform()
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR,'#global-nav-typeahead > input').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR,'#global-nav-typeahead > input').send_keys(keyword)
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR,'#global-nav-typeahead > input').send_keys(Keys.ENTER)
        time.sleep(5)

        driver.find_element(By.CSS_SELECTOR,'#search-reusables__filters-bar ul li button').click()
        time.sleep(5)

        driver.find_element(By.CSS_SELECTOR,
                            '#search-reusables__filters-bar > div > div > button').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            '#artdeco-modal-outlet .list-style-none.flex-1 li:nth-child(2) ul li:nth-child(2) label').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            '#artdeco-modal-outlet .list-style-none.flex-1 li:nth-child(3) ul li:nth-child(2) label').click()

        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            '#artdeco-modal-outlet .justify-flex-end.display-flex.mv3.mh2 button:nth-child(2)').click()
        time.sleep(2)
        currhight = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == currhight:
                break
            currhight = new_height
        totalPosts = driver.find_elements(By.CSS_SELECTOR,'.search-results-container .feed-shared-update-v2.feed-shared-update-v2--minimal-padding.full-height.relative.artdeco-card')
        for post in totalPosts:
            poston = post.find_element(By.CSS_SELECTOR,'.feed-shared-actor.display-flex.feed-shared-actor--with-control-menu a .feed-shared-actor__sub-description.t-12.t-normal.t-black--light span span').text.split('•')[0].strip()
            if '1d' in poston or 'm' in poston or 'h' in poston or 'now' in poston:
                if 'mo' not in poston:
                    element = post.find_element(By.CSS_SELECTOR,
                                      '.feed-shared-control-menu.feed-shared-update-v2__control-menu.absolute.text-align-right')
                    actions = ActionChains(driver)
                    actions.move_to_element(element).perform()
                    time.sleep(1)
                    post.find_element(By.CSS_SELECTOR,
                                      '.feed-shared-control-menu.feed-shared-update-v2__control-menu.absolute.text-align-right').click()
                    time.sleep(1)
                    post.find_element(By.CSS_SELECTOR,
                                      '.feed-shared-control-menu.feed-shared-update-v2__control-menu.absolute.text-align-right div[aria-label="Control Menu Options"] li:nth-child(2)').click()

                    time.sleep(1)
                    posturl = driver.find_element(By.CSS_SELECTOR,'.artdeco-toast-item.artdeco-toast-item--visible.ember-view a.artdeco-toast-item__cta').get_attribute('href')

                    #posturl = post.find_element(By.CSS_SELECTOR,'.feed-shared-actor.display-flex.feed-shared-actor--with-control-menu a').get_attribute('href')
                    postUrl.append(f'Keyword no.{i+1}:  '+posturl)
    if len(postUrl)!=0:
        for url in postUrl:
            fileoutput.write(url+'\n')
            fileoutput.flush()

    driver.quit()
    if len(postUrl)!=0:
        email()