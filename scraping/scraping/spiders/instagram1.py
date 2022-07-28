import requests
import scrapy
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import csv
import re

post = []
headers = ['url', 'country', 'engagementRate', 'name', 'Destination(local)', 'Followers', 'Total Posts', 'Video Posts', 'Date of first post', 'Gender', 'Engagement rate for video posts', 'Avg Likes', 'Avg Comments', 'Number of total posts with ads', 'Number of video posts with ads', 'Gender of engagers (female/male)', 'E-Mail', 'Categories/topicsl', 'Audience countries', ]
fileout = open('intagram.csv','w',newline='',encoding='utf-8')
writer = csv.DictWriter(fileout,fieldnames=headers)
writer.writeheader()


def instalogin():
    driver.get('https://www.instagram.com/')
    time.sleep(3)
    driver.find_element_by_css_selector('input[name="username"]').send_keys(insta_email)
    driver.find_element_by_css_selector('input[name="password"]').send_keys(insta_password)
    Login_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  '// button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '// button[contains(text(), "Not Now")]'))).click()


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

def do_scroll(driver):
    global vcount
    lastscrolled = 0
    scroll_pause_time = 15
    last_height = driver.execute_script("return document.body.scrollHeight")
    totalturns = 0
    while True:
        # if totalturns>20:
        #     break
        # else:
        #     totalturns+=1
        i = 0
        for cnt,res in enumerate(driver.find_elements_by_css_selector("div._2z6nI div.v1Nh3.kIKUG._bz0w")[lastscrolled:]):
            urldict= dict()
            hover = ActionChains(driver).move_to_element(res)
            hover.perform()
            try:
                if res.find_element_by_css_selector('a div.u7YqG svg').get_attribute('aria-label') == "Video":
                    vcount+=1
            except:
                pass
            try:
                likes = res.find_element_by_css_selector('a div.qn-0x').text.split('\n')[0]
            except:
                pass
            try:
                like = convert_str_to_number(likes)
            except:
                like = int(likes.replace(',',''))
            try:
                Comment = res.find_element_by_css_selector('a div.qn-0x').text.split('\n')[1]
            except:
                pass
            try:
                comnt = convert_str_to_number(Comment)
            except:
                comnt = int(Comment.replace(',',''))
            url = res.find_element_by_css_selector('a').get_attribute('href')
            urldict[url]= [like, comnt]
            post.append(urldict)
            i = cnt
        lastscrolled +=i
        if lastscrolled>33:
            lastscrolled = 21
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver


if __name__ == '__main__':
    i = 1
    insta_file = open('insta-credentials.txt', 'r')
    insta_creds = insta_file.read().split('\n')
    insta_email = insta_creds[0]
    insta_password = insta_creds[1]
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    instalogin()
    while i <= 10:
        vcount = 0
        url = f'https://starngage.com/app/global/influencer/ranking/germany?page={i}'
        i += 1
        req = requests.get(url=url)
        resp = scrapy.Selector(text=req.content.decode('utf-8'))
        for tr in resp.css('table tbody tr')[4:]:
            item = dict()
            item['url'] = tr.css('td a::text').extract_first().replace('@', '')
            item['country'] = tr.css('td:nth-child(4) a::text').extract_first()
            item['engagementRate'] = tr.css('td:nth-child(7)::text').extract_first()
            url = f"https://www.instagram.com/{item['url']}/"
            driver.get(url)
            while driver.current_url != url:
                driver.get(url)
            ps = driver.page_source
            responce = scrapy.Selector(text=ps)
            item['name'] = responce.css('section.zwlfE h2::text').extract_first()
            item['Destination(local)'] = ''
            data = [' '.join(v.css('::text').extract()) for v in responce.css('.k9GMp .Y8-fY ')]
            item['Followers'] = [v.replace('followers', '').strip() for v in data if 'follower' in v][0] if [v.replace('followers', '').strip() for v in data if 'follower' in v] else ''
            item['Total Posts'] = [v.replace('posts', '').strip() for v in data if 'post' in v][0] if [v for v in data if 'post' in v] else ''
            driver.maximize_window()
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,15);")
            last_height = driver.execute_script("return document.body.scrollHeight")
            do_scroll(driver)
            sumlike=0
            commentnumber = 0
            countlikes=0
            countcomment=0
            res = []
            [res.append(x) for x in post if str(x.keys()).split('[\'')[1].split('\']')[0] not in (set().union(*(x.keys() for x in res)))]
            for a in res:
                sumlike = sumlike + list(a.values())[0][0]
                countlikes += 1
                commentnumber = commentnumber+list(a.values())[0][1]
                countcomment += 1
            driver.get(list(res[-1].keys())[0])
            try:
                date = driver.find_element_by_xpath('.//div[@class="k_Q0X I0_K8  NnvRN"]').text
            except:
                date = 'not available'
            item['Date of first post'] = date
            item['Video Posts'] = vcount
            item['Gender'] = ''
            item['Engagement rate for video posts'] = ''
            item['Avg Likes'] = int(sumlike/countlikes)
            item['Avg Comments'] = int(commentnumber/countcomment)
            item['Number of total posts with ads'] = ''
            item['Number of video posts with ads'] = ''
            item['Gender of engagers (female/male)'] = ''
            match = re.search(r'[\w\.-]+@[\w\.-]+', ' '.join(responce.css('::text').extract()))
            try:
                item['E-Mail'] = match.group(0)
            except:
                item['E-Mail'] = ''
            item['Categories/topicsl'] = ''
            item['Audience countries'] = ''
            writer.writerow(item)
            fileout.flush()
    driver.close()