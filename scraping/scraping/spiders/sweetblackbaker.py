try:
    import pkg_resources.py2_warn
except ImportError:
    pass
import datetime
import json
import time

import dateutil.parser
import pytz
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjY0YjU1MTEyLWYxZGMtNDM4OS1hYzA4LWM0NGVjMGQ1NWU1NyIsImV4cCI6MTYyODUzNzIxNywiaXNzIjoidGV4dHZlcmlmaWVkLmNvbSIsImF1ZCI6InRleHR2ZXJpZmllZC5jb20ifQ.jZYsr3A3ZGuZqIcf4ft5JmZzM_ix5GlOSjFpm7Uk4b
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjY0YjU1MTEyLWYxZGMtNDM4OS1hYzA4LWM0NGVjMGQ1NWU1NyIsImV4cCI6MTYyODUzODkxMCwiaXNzIjoidGV4dHZlcmlmaWVkLmNvbSIsImF1ZCI6InRleHR2ZXJpZmllZC5jb20ifQ.Ai0oIitfL1JmLhHsbxCwFFqDgc9gPZ-1HAfJocQmwgk
if __name__ == '__main__':
    BTfile = open('textverifiedbearartoken.txt', 'r')
    BTfileread = json.loads(BTfile.read())
    BTfile.close()

    IDFileread = open('textverifiedID.txt', 'r')
    IDFileappend = open('textverifiedID.txt', 'a+')

    UnDoneUrls = open('undoneUrl.txt','w')

    currentdatetime = datetime.datetime.now(pytz.timezone("America/New_York"))
    inputfile = open('websiteName.txt', 'r')
    inputlist = inputfile.read().split('\n')
    headers = {
        'X-SIMPLE-API-ACCESS-TOKEN': '1_X4fT1jwm8i2SYq2psZqCqYHR_GzYhOuhvysEw2C4XU_J-y2JO5A8yTfyv4wcGBJirXEqFABn'
    }
    BASEURL = 'https://www.textverified.com/Api'
    if currentdatetime > dateutil.parser.isoparse(BTfileread['expiration']):
        res = requests.post(BASEURL + '/SimpleAuthentication', headers=headers)
        Barer_token = json.loads(res.text)['bearer_token']
        bearerheader = {'authorization': f"Bearer {Barer_token}"}
        BTfile = open('textverifiedbearartoken.txt', 'w')
        BTfilewrite = BTfile.write(res.text)
        BTfile.close()
        headr = {
            'authorization': f"Bearer {Barer_token}",
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

    else:
        bearerheader = {'authorization': f"Bearer {BTfileread['bearer_token']}"}
        headr = {
            'authorization': f"Bearer {BTfileread['bearer_token']}",
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    payload = "{\"id\":15}"

    ResurrectFlag = False
    for d in IDFileread.read().split('\n'):
        if d == '':
            continue
        response = requests.put(BASEURL + f'/Verifications/{d}/Resurrect', '')
        if response.status_code == 200:
            try:
                phone = json.loads(response.text)['number']
                id = json.loads(response.text)['id']
                ResurrectFlag = True
                break
            except:
                pass
        elif response.status_code == 429:
            rr = requests.get(BASEURL + '/Verifications/Pending', headers=bearerheader)
            try:
                id = json.loads(rr.text)['id']
                response = requests.get(BASEURL + f'/Verifications/{id}', headers=bearerheader)
                phone = json.loads(response.text)['number']
                ResurrectFlag = True
                break
            except:
                pass
        elif response.status_code==400 or response.status_code==401 or response.status_code==404:
            pass
    if ResurrectFlag == False:
        response = requests.post(BASEURL + '/Verifications', data=payload, headers=headr)
        if response.status_code == 200:
            id = json.loads(response.text)['id']
            phone = json.loads(response.text)['number']
            IDFileappend.write(id + '\n')
        elif response.status_code == 429:
            rr = requests.get(BASEURL+'/Verifications/Pending', headers = bearerheader)
            id = json.loads(rr.text)['id']
            response = requests.get(BASEURL+f'/Verifications/{id}', headers = bearerheader)
            phone = json.loads(response.text)['number']
        else:
            pass

    for i, url in enumerate(inputlist[1:]):
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        if url == '':
            continue
        driver.get(url)
        driver.switch_to.frame(driver.find_element_by_id('ci_CouponsClickParentIframe'))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]')))
        driver.find_element_by_css_selector('input[type="checkbox"]').click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#page-control button')))
        driver.find_element_by_css_selector('#page-control button').click()
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.inputSign')))
            # phone = json.loads(response.text)['number']
            driver.find_element_by_css_selector('input.inputSign').send_keys(phone)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button#buttonSendVerify')))
            time.sleep(0.5)
            driver.find_element_by_css_selector('button#buttonSendVerify').click()
            try:
                if 'Your phone number could not be accepted' in driver.find_element_by_css_selector('.error span').text:
                    driver.find_element_by_css_selector('input[placeholder="Your phone number"]').clear()
                    RFlag = False
                    for d in IDFileread.read().split('\n'):
                        if d == '':
                            continue
                        response = requests.put(BASEURL + f'/Verifications/{d}/Resurrect', '')
                        if response.status_code == 200:
                            try:
                                phone = json.loads(response.text)['number']
                                id = json.loads(response.text)['id']
                                RFlag = True
                                break
                            except:
                                pass
                        elif response.status_code == 429:
                            rr = requests.get(BASEURL + '/Verifications/Pending', headers=bearerheader)
                            try:
                                id = json.loads(rr.text)['id']
                                response = requests.get(BASEURL + f'/Verifications/{id}', headers=bearerheader)
                                phone = json.loads(response.text)['number']
                                RFlag = True
                                break
                            except:
                                pass
                        elif response.status_code == 400 or response.status_code == 401 or response.status_code == 404:
                            pass
                    if RFlag == False:
                        response = requests.post(BASEURL + '/Verifications', data=payload, headers=headr)
                        if response.status_code == 200:
                            id = json.loads(response.text)['id']
                            phone = json.loads(response.text)['number']
                            IDFileappend.write(id + '\n')
                        elif response.status_code == 429:
                            rr = requests.get(BASEURL + '/Verifications/Pending', headers=bearerheader)
                            id = json.loads(rr.text)['id']
                            response = requests.get(BASEURL + f'/Verifications/{id}', headers=bearerheader)
                            phone = json.loads(response.text)['number']
                        else:
                            pass
                    time.sleep(5)
                    driver.find_element_by_css_selector('input.inputSign').send_keys(phone)
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button#buttonSendVerify')))
                    time.sleep(0.5)
                    driver.find_element_by_css_selector('button#buttonSendVerify').click()
            except:
                pass
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#verifyCodeField')))
            while True:
                verificationcode = ''
                ress = requests.get(BASEURL + f'/Verifications/{id}', headers=bearerheader)
                verificationcode = json.loads(ress.text)['code']
                if verificationcode == None:
                    ress = requests.put(BASEURL+f'/Verifications/{id}/Reuse', headers=bearerheader)
                    time.sleep(5)
                    ress = requests.get(BASEURL + f'/Verifications/{id}', headers=bearerheader)
                    verificationcode = json.loads(ress.text)['code']
                    break
                else:
                    break
            driver.find_element_by_css_selector('#verifyCodeField').send_keys(verificationcode)
            time.sleep(0.5)
            driver.find_element_by_css_selector('.inputArea button').click()
            time.sleep(5)
            unable = False
            while True:
                try:
                    if 'Sorry, that code is not valid.' in driver.find_element_by_css_selector('.error').text:
                        UnDoneUrls.write(driver.current_url+'\n')
                        print(f'Couldent complete {driver.current_url}')
                        driver.quit()
                        unable = True
                except:
                    break
            if unable == False:
                while True:
                    try:
                        if 'Your coupons are printing' in driver.find_element_by_css_selector('h1').text:
                            time.sleep(5)
                    except:
                        break
                time.sleep(5)
                try:
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.close()
                    while True:
                        selection = input('Please Press Enter in your other program then press enter in here')
                        if selection == '':
                            break
                    driver.switch_to.window(driver.window_handles[0])
                    driver.quit()
                except:
                    pass
            else:
                continue
        except:
            driver.quit()
    UnDoneUrls.close()



    # driver.quit()

    print('done')
