from selenium import webdriver
import scrapy
from selenium.webdriver.common.keys import Keys
from typing import Any, Union
import time
import csv

header = ['search Term', 'tweet handle', 'tweet time', 'tweet retweets', 'tweet likes', 'tweet text']
file = open('twitterWordSearch.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()
inputfile = open('twitterWordSearchInput.txt', 'r')
inp = inputfile.readlines()
responcelist = []


def getPage():
    driver = webdriver.Firefox()
    driver.get('https://twitter.com/')
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/a[2]/div').click()
    time.sleep(3)
    driver.find_element_by_xpath(
        '/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input').send_keys(
        'usamaahmad13')  # enter username
    driver.find_element_by_xpath(
        '/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input').send_keys(
        'manzoor007')  # enter pasword
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div').click()
    time.sleep(3)

    for line in inp:
        searchKey = line.split(' ')[0]
        endDate = line.split(' ')[1]
        startDate = line.split(' ')[2]
        try:
            driver.find_element_by_xpath(
                '/html/body/div/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(
                searchKey + ' until:' + endDate + ' since:' + startDate)
            driver.find_element_by_xpath(
                '/html/body/div/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(
                Keys.RETURN)
        except:
            driver.find_element_by_xpath(
                '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input').clear()
            driver.find_element_by_xpath(
                '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(
                searchKey + ' until:' + endDate + ' since:' + startDate)
            driver.find_element_by_xpath(
                '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(
                Keys.RETURN)
            driver.refresh()
            time.sleep(2)
        scroll_pause_time = 5
        last_height: Union[Union[int, str], Any] = driver.execute_script("return document.body.scrollHeight")
        while True:
            ps = driver.page_source
            resp = scrapy.Selector(text=ps)
            for ls in resp.css(
                    'div[class="css-1dbjc4n"] div[class="css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll r-1ny4l3l"]'):
                responcelist.append(ls)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        for response in responcelist:
            if response.css('div[class="css-1dbjc4n r-1wtj0ep r-1j3t67a r-1w50u8q"]'):
                continue
            if response.css('div[data-testid="UserCell"]'):
                continue
            if response.css(
                    'a[class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1ny4l3l r-1j3t67a r-9qu9m4 r-o7ynqc r-6416eg"]'):
                continue
            try:
                if response.css(
                        'div[class="css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2"] span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0" ]::text').extract()[
                    1] == '·':
                    continue
            except:
                continue
            item = dict()
            item['search Term'] = searchKey
            item['tweet handle'] = response.css(
                'div[class="css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2"] span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0" ]::text').extract()[
                1]
            item['tweet time'] = response.css(
                'div[class="css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2"] a::attr(title)').extract_first()
            item['tweet text'] = ' '.join(response.css(
                'div[class="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"] ::text').extract())
            try:
                item['tweet retweets'] = response.css(
                    'div[class="css-1dbjc4n r-18u37iz r-1wtj0ep r-156q2ks r-1mdbhws"] div[data-testid="retweet"] span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]::text').extract_first()
            except:
                item['tweet retweets'] = 0
            try:
                item['tweet likes'] = response.css(
                    'div[class="css-1dbjc4n r-18u37iz r-1wtj0ep r-156q2ks r-1mdbhws"] div[data-testid="like"] span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]::text').extract_first()
            except:
                item['tweet likes'] = 0
            writer.writerow(item)
            file.flush()
        responcelist.clear()
    driver.quit()


if __name__ == '__main__':
    getPage()
