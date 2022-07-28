# from tweepy import API
# from tweepy import OAuthHandler
#
# ACCESS_TOKEN = "3728211501-5CydVErDpAnbsi4HgUFDutK9JheWYDV0CPhazYW"
# ACCESS_TOKEN_SECRET = "xLtXrlVE1vi7VIzGfFK15EymFqCTBm5PCMkEcHGFDsbOz"
# CONSUMER_KEY = "oPlHbnjm6jyx0bZJCqp1sIdZN"
# CONSUMER_SECRET = "FeXG9Dc2BBEjFiRTfLS06GMe0ZGPEIrWeYFSh6TLdujbxyZgQB"
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as ff_options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    followingfileappend = open('twitter_following.txt', 'a', encoding='utf-8')
    followingfileread = open('twitter_following.txt', 'r', encoding='utf-8')
    alreadyFollowed = followingfileread.read().split('\n')
    fileinput = open('twitter_handles_.txt', 'r')
    finput = fileinput.read().split(' ')
    usernamefile = open('twitter_pwd.txt','r')
    usernamef =usernamefile.read().split('\n')
    start, end = 0,5000
    usernamef.reverse()
    for usepwd in usernamef:
        driver = webdriver.Chrome()
        driver.get("https://www.twitter.com")
        driver.maximize_window()
        driver.find_element_by_css_selector('a[data-testid="loginButton"]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('input[name="session[username_or_email]"]').send_keys(usepwd.split(' ')[0])
        time.sleep(1)
        driver.find_element_by_css_selector('input[name="session[password]"]').send_keys(usepwd.split(' ')[1])
        time.sleep(1)
        driver.find_element_by_css_selector('div[data-testid="LoginForm_Login_Button"]').click()
        start +=5000
        end +=5000
        iterator = 0
        for us in finput[start:end]:
            print(usepwd)
            if us == '':
                continue
            if us in alreadyFollowed:
                continue
            print(iterator)
            driver.get(f'https://www.twitter.com/{us}')
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="placementTracking"]')))
            except:
                pass
            time.sleep(1)
            followingfileappend.write(f'{us}\n')
            followingfileappend.flush()
            try:
                if 'Following' in driver.find_element_by_css_selector('div[data-testid="placementTracking"] span').text:
                    continue
                else:
                    iterator += 1
                    time.sleep(1)
                    driver.find_element_by_css_selector('div[data-testid="placementTracking"] ').click()
                    time.sleep(5)
                    if 'Following' not in driver.find_element_by_css_selector('div[data-testid="placementTracking"] span').text:
                        iterator = 0
                        flag = True
                        break
            except:
                continue
            if iterator%10 ==0:
                time.sleep(15)
            if iterator == 390:
                iterator = 0
                flag = True
                break
        driver.quit()











    # auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # api = API(auth, wait_on_rate_limit=True)
    # try:
    #     api.verify_credentials()
    #     print("Authentication OK")
    # except:
    #     print("Error during authentication")

    #     try:
    #         user = api.get_user(us)
    #         print("The screen name corresponds to the user with the name : " + user.name)
    #     except:
    #         continue
    #     try:
    #         user.follow()
    #     except:
    #         print('some error occured')
    #         continue
