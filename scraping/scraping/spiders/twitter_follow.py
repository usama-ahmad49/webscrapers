import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def do_scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    i = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i += 1
        if i == 20:
            i = 0
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    return driver


if __name__ == '__main__':
    textsearchfile = open('twittertextsearch.txt', 'r')
    textsearchkeywords = textsearchfile.read().split('\n')
    usernamefile = open('twitter_pwd.txt', 'r')
    usernamef = usernamefile.read().split('\n')
    driver = webdriver.Chrome()
    driver.get("https://www.twitter.com")
    driver.maximize_window()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="loginButton"]')))
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'a[data-testid="loginButton"]').click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]').send_keys(usernamef[0])
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[-3].click()
    try:
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]').send_keys(usernamef[-1])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[data-testid="ocfEnterTextNextButton"]').click()
    except:
        pass
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]').send_keys(usernamef[1])
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]')))
    driver.find_element(By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]').click()
    time.sleep(5)
    followcount = 0
    for word in textsearchkeywords:
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search query"]').click()
        time.sleep(0.5)
        try:
            driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Clear"]').click()
            time.sleep(0.5)
        except:
            pass
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search query"]').send_keys(word)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search query"]').send_keys(Keys.ENTER)
        time.sleep(2)
        # do_scroll(driver)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] article')))
        except:
            continue
        for i in range(0,20):
            for post in driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] article'):
                a = ActionChains(driver)
                try:
                    elem = post.find_element(By.CSS_SELECTOR, 'a[role="link"]')
                    driver.execute_script("arguments[0].scrollIntoView(false);", elem)
                    a.move_to_element(elem).perform()
                    time.sleep(0.5)
                    if driver.find_element(By.ID, 'layers').find_element(By.CSS_SELECTOR, 'div[data-testid="HoverCard"] div[role="button"]').text == 'Follow':
                        driver.find_element(By.ID, 'layers').find_element(By.CSS_SELECTOR, 'div[data-testid="HoverCard"] div[role="button"]').click()
                        followcount+=1
                        time.sleep(3)
                    else:
                        time.sleep(1)
                except:
                    pass

                if followcount == 400:
                    break
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            if followcount == 400:
                break

        if followcount == 400:
            break

    driver.quit()
