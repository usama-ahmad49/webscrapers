import requests
import scrapy
from seleniumwire import webdriver
import time
import csv
headers = ['url', 'country', 'engagementRate', 'name', 'Destination(local)', 'Followers', 'Total Posts', 'Video Posts', 'Date of fist post', 'Gender', 'Engagement rate for video posts', 'Avg Likes', 'Avg Comments', 'Number of total posts with ads', 'Number of video posts with ads', 'Gender of engagers (female/male)', 'E-Mail', 'Categories/topicsl', 'Audience countries', ]
fileout = open('intagram.csv','w',newline='',encoding='utf-8')
writer = csv.DictWriter(fileout,fieldnames=headers)
writer.writeheader()


def instalogin():
    driver.get('https://www.instagram.com/')
    time.sleep(3)
    driver.find_element_by_css_selector('input[name="username"]').send_keys(insta_email)
    driver.find_element_by_css_selector('input[name="password"]').send_keys(insta_password)
    time.sleep(2)
    driver.find_element_by_css_selector('button[type="submit"]').submit()
    time.sleep(10)
    if 'Save Your Login Info?' in driver.find_element_by_css_selector('.ABCxa div.JErX0 .olLwo').text:
        driver.find_element_by_css_selector('.cmbtv button').click()
        time.sleep(10)

if __name__ == '__main__':
    i = 1
    insta_file = open('insta-credentials.txt', 'r')
    insta_creds = insta_file.read().split('\n')
    insta_email = insta_creds[0]
    insta_password = insta_creds[1]
    driver = webdriver.Chrome()
    instalogin()
    while i <= 10:
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
            item['Followers'] = responce.css('section.zwlfE a span::text').extract()[1]
            item['Total Posts'] = responce.css('section.zwlfE a span::text').extract()[0]
            item['Video Posts'] = ''
            item['Date of fist post'] = ''
            item['Gender'] = ''
            item['Engagement rate for video posts'] = ''
            item['Avg Likes'] = ''
            item['Avg Comments'] = ''
            item['Number of total posts with ads'] = ''
            item['Number of video posts with ads'] = ''
            item['Gender of engagers (female/male)'] = ''
            item['E-Mail'] = ''
            item['Categories/topicsl'] = ''
            item['Audience countries'] = ''
            writer.writerow(item)
            fileout.flush()
    driver.close()