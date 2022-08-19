import requests
import json
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from seleniumwire import webdriver


def main():
    options = {"disable_encoding": True}

    driver = webdriver.Chrome(seleniumwire_options=options)
    driver.maximize_window()
    driver.get('https://twitter.com/')
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, 'div.css-901oao.r-1awozwy.r-1cvl2hr.r-6koalj.r-18u37iz').click()
    time.sleep(3)

    inputEmail = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
    time.sleep(2)
    inputEmail.send_keys('rixtysoft01@gmx.com')
    time.sleep(2)
    inputEmail.send_keys(Keys.ENTER)
    try:
        inputuser = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
        time.sleep(2)
        inputuser.send_keys('samiyaahmad16')
        time.sleep(2)
        inputuser.send_keys(Keys.ENTER)
    except:
        pass

    inputPass = driver.find_elements(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')[-1]
    time.sleep(2)
    inputPass.send_keys('qwerty1234uiop')
    time.sleep(3)
    inputPass.send_keys(Keys.ENTER)
    time.sleep(3)

    searchWord = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
    time.sleep(2)
    searchWord.send_keys('crypto')
    time.sleep(2)
    searchWord.send_keys(Keys.ENTER)
    resp = [v for v in driver.requests if'adaptive.json' in v.url][0]
    body = json.loads(resp.response.body.decode())

    for link in (list(body['globalObjects']['users'].values())):
        tweeturl = link['screen_name']
        tweet_resp = requests.get(f'https://twitter.com/{tweeturl}')
        tweet_data = scrapy.Selector(text=tweet_resp.text)


if __name__ == "__main__":
    main()
