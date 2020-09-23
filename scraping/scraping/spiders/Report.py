import os
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
import scrapy
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth_oauthlib.flow import InstalledAppFlow
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret_tv.json'


def get_service() :
    flow = InstalledAppFlow.from_client_secrets_file ( CLIENT_SECRETS_FILE, SCOPES )
    arguments = {'prompt': 'consent'}
    auth_url = flow.authorization_url(**arguments)[0] + '&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
    # credentials = flow.run_console ()
    get_driver('rixtysoft01@gmail.com','qwerty123uiop',auth_url)
    return auth_url

def get_driver(username, password, auth_url):   # to get auth_url into get_driver
    options=Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Firefox()   #yahan p ye error aa rha hai (module 'selenium.webdriver.chrome.webdriver' has no attribute 'Chrome')
    driver.get(auth_url)
    time.sleep(5)
    username_field = driver.find_element_by_name('identifier')
    username_field.send_keys(username)
    time.sleep(2)
    submit=driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button')
    submit.click()
    time.sleep(5)
    password_field = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    password_field.send_keys(password)
    time.sleep(2)
    submit = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button')
    submit.click()
    time.sleep(5)
    submit=driver.find_element_by_xpath('//*[@id="oauthScopeDialog"]/div[3]/div[1]')
    submit.click()
    time.sleep(5)
    submit = driver.find_element_by_xpath('//*[@id="submit_approve_access"]/div/button')
    submit.click()
    time.sleep(5)
    #code=driver.find_element_by_css_selector('textarea.qBHUIf').text
    responce = scrapy.Selector('textarea.qBHUIf' + driver.page_source)
    #driver.quite()
    return driver

#needs to move text from responce to
def execute_api_request(client_library_function, **kwargs) :
    response = client_library_function (
        **kwargs
    ).execute ()

    print ( response )


if __name__ == '__main__' :
    # Disable OAuthlib's HTTPs verification when running locally.
    # *DO NOT* leave this option enabled when running in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'

    youtubeAnalytics = get_service ()
    execute_api_request (
        youtubeAnalytics.reports ().query,
        ids='channel==MINE',
        startDate='2020-07-19',
        endDate='2020-07-23',
        metrics='views,comments,likes,estimatedMinutesWatched,subscribersGained',
        dimensions='day',
        sort='day',
    )
