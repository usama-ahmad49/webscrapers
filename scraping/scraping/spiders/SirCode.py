try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import scrapy
import json
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as ff_options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import datefinder
import pytz
utc=pytz.UTC

csv_columns = ['keyword', 'date', 'title', 'link']
csvfile = open('algoliaArticle.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


def create_driver():
    """
    creates firefox and chrome drivers
    """
    random_proxy = "142.54.161.98:19004"
    options = ff_options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-javascript')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--width=1024')
    options.add_argument('--height=768')
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": random_proxy,
        "ftpProxy": random_proxy,
        "sslProxy": random_proxy
    }
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.peerconnection.enabled", False)
    profile.set_preference("media.navigator.enabled", False)
    # profile.set_preference("general.useragent.override", user_agent)
    profile.update_preferences()

    driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=profile,
                               firefox_options=options)
    return driver


def get_driver():
    random_proxy = "142.54.161.98:19004"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-javascript')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--width=1024')
    options.add_argument('--height=768')
    firefox_capabilities = webdriver.DesiredCapabilities.CHROME
    firefox_capabilities['marionette'] = True
    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": random_proxy,
        "ftpProxy": random_proxy,
        "sslProxy": random_proxy
    }
    driver = webdriver.Chrome(desired_capabilities=firefox_capabilities, chrome_options=options)
    return driver


def make_request(url):
    tries = 5
    global driver
    while tries:
        try:
            driver.get(url)
            while not [v for v in driver.requests if 'Item_production_sort_date' in v.url]:
                time.sleep(1)
            req = [v for v in driver.requests if 'Item_production_sort_date' in v.url][-1]
            data = json.loads(req.response.body.decode('utf-8'))
            return data
        except:
            driver.close()
            driver = create_driver()
            tries -= 1
    return None


def double_check(to_find, link):
    global proxy_driver
    proxy_driver.get(link)
    # time.sleep(5)
    response = scrapy.Selector(text=proxy_driver.page_source)
    while not response.css('::text').extract():
        proxy_driver.close()
        time.sleep(30)
        proxy_driver = create_driver()
        proxy_driver.get(link)
        response = scrapy.Selector(text=driver.page_source)

    text = ' '.join(response.css('::text').extract())
    words = [v.lower() for v in text.lower().split() if v]
    if to_find.lower() in words:
        return True
    else:
        return False


def check_data(hits, to_find):
    for hit in hits:
        keyword = to_find.split(' ')
        words = hit['title'].lower().split()
        lenkeyword = len(keyword)
        try:
            if keyword[0].lower() in hit['title'].lower():
                index = words.index(keyword[0].lower())
                for i in range(lenkeyword - 1):
                    if keyword[i + 1].lower() == words[index + 1]:
                        index = index + 1

                # words = [v.lower() for v in hit['title'].lower().split() if v]
                if index == words.index(keyword[0]) + (len(keyword) - 1):
                    item = dict()
                    item['keyword'] = to_find
                    item['date'] = hit['created_at']
                    item['title'] = hit['title']
                    item['link'] = 'https://news.ycombinator.com/item?id={}'.format(hit['objectID'])
                    writer.writerow(item)
                    csvfile.flush()
            else:
                if double_check(to_find, 'https://news.ycombinator.com/item?id={}'.format(hit['objectID'])):
                    item = dict()
                    item['keyword'] = to_find
                    item['date'] = hit['created_at']
                    item['title'] = hit['title']
                    item['link'] = 'https://news.ycombinator.com/item?id={}'.format(hit['objectID'])
                    writer.writerow(item)
                    csvfile.flush()
        except:
            pass


def send_email():
    import datetime
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    obj = smtplib.SMTP(host='Smtp.gmail.com', port=587, timeout=1000)
    obj.starttls()
    obj.ehlo()
    msg = MIMEMultipart()
    filename = 'algoliaArticle.csv'
    file = open('credentials.txt', 'r')
    file_data = file.read()
    file_data = file_data.split('\n')

    msg['Subject'] = "{}{}".format(filename, datetime.datetime.now())
    password = file_data[1]
    obj.login(file_data[0], password)
    with open(filename, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=filename))

    obj.sendmail(file_data[0], file_data[2], msg.as_string())
    obj.quit()


def refresh_drivers():
    global proxy_driver
    global proxy_pages_count
    proxy_pages_count = 0
    proxy_driver.close()
    proxy_driver = create_driver()


if __name__ == '__main__':
    # import requests
    # requests.get('https://shift.com/cars/oregon', proxies={"http": 'http://142.54.161.98:19004'})
    proxy_pages_count = 0
    driver = get_driver()
    proxy_driver = create_driver()
    # driver = get_driver()
    file = open('readData.txt', 'r')
    file_data = file.read().split('\n')
    dateData = file_data[0]
    target_date = datetime.now() - timedelta(days=int(dateData))
    target_date = utc.localize(target_date)
    for fileData in file_data[1:]:
        url = 'https://hn.algolia.com/?dateRange=all&page=0&prefix=false&query=' + fileData + '&sort=byDate&type=story'
        data = make_request(url)
        if not data:
            continue
        pages = data['nbPages']
        check_data(data['hits'], fileData)
        if target_date < list(datefinder.find_dates(data['hits'][-1]['created_at']))[0]:
            for page_no in range(2, pages):
                url = 'https://hn.algolia.com/?dateRange=all&page=' + str(page_no) + '&prefix=false&query=' + fileData + '&sort=byDate&type=story'

                data = make_request(url)
                if not data:
                    continue
                check_data(data['hits'], fileData)
                print(list(datefinder.find_dates(data['hits'][-1]['created_at']))[0])
                if target_date > list(datefinder.find_dates(data['hits'][-1]['created_at']))[0]:
                    break

        driver.close()
        driver = get_driver()

    try:
        send_email()
    except:
        pass

