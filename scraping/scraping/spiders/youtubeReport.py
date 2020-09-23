import os
import time
import json
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import scrapy
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret_tv.json'

google_sheet_url = (
    'https://docs.google.com/spreadsheets/u/0/d/1sw_DpejPFlZ1dqf6jJSGWI_8DH2CGsaN6VAxIb9hmkI/export?format=csv&id=1sw_DpejPFlZ1dqf6jJSGWI_8DH2CGsaN6VAxIb9hmkI&gid=0')

class youtubeReport():
    def open_spider(self, responce):
        response = requests.get(self.google_sheet_url)
        self.companies = response.content.decode('utf-8').split()


    def get_service(self, response):
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        arguments = {'prompt': 'consent'}
        auth_url = flow.authorization_url(**arguments)[0] + '&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
        self.get_driver('rixtysoft01@gmail.com', 'qwerty123uiop', auth_url)
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def get_driver(username, password, auth_url):  # to get auth_url into get_driver
        options = Options()
        options.add_argument('--disable-notifications')
        driver = webdriver.Firefox()
        driver.get(auth_url)
        time.sleep(5)
        username_field = driver.find_element_by_name('identifier')
        username_field.send_keys(username)
        time.sleep(2)
        submit = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button')
        submit.click()
        time.sleep(5)
        password_field = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password_field.send_keys(password)
        time.sleep(2)
        submit = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button')
        submit.click()
        time.sleep(5)
        submit = driver.find_element_by_xpath('//*[@id="oauthScopeDialog"]/div[3]/div[1]')
        submit.click()
        time.sleep(5)
        submit = driver.find_element_by_xpath('//*[@id="submit_approve_access"]/div/button')
        submit.click()
        time.sleep(5)
        code=driver.find_element_by_css_selector('textarea.qBHUIf').getText()
        responce = scrapy.Selector('textarea.qBHUIf' + driver.page_source)
        # driver.quite()
        return driver


    def execute_api_request(client_library_function, **kwargs):
        response = client_library_function(
            **kwargs
        ).execute()

        print ( response )


    def parse(self, responce):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
        auth = self.get_service()
        while True:
            query = self.execute_api_request(auth.reports().query,
                                        ids='channel==MINE',
                                        startDate='2020-07-19',
                                        endDate='2020-07-23',
                                        metrics='views,comments,likes,shares,estimatedMinutesWatched,subscribersGained',
                                        dimensions='day',
                                        sort='day',
                                        )
            data=json.loads(query)


# if __name__ == '__main__':
#   # Disable OAuthlib's HTTPs verification when running locally.
#   # *DO NOT* leave this option enabled when running in production.
#   # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#
#   youtubeAnalytics = get_service()
#   execute_api_request(
#       youtubeAnalytics.reports().query,
#       ids='channel==MINE',
#       startDate='2017-01-01',
#       endDate='2017-12-31',
#       metrics='estimatedMinutesWatched,views,likes,shares,subscribersGained',
#       dimensions='day',
#       sort='day'
#   )
