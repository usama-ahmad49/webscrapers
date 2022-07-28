from selenium import webdriver
import scrapy
import time
import csv
import requests
import re
from threading import Thread
import mysql.connector
import unidecode


headers = ['name', 'address', 'email', 'website', 'telephone', 'search_term']
fileoutput = open('googlemaps.csv', 'a', newline='', encoding='utf-8')
writer = csv.DictWriter(fileoutput, fieldnames=headers)
# writer.writeheader()

emails = []


def do_scroll(driver):
    scroll_pause_time = 5
    last_height = len(driver.find_elements_by_css_selector(f'div[aria-label="Ergebnisse für {searchTerm}"] a'))
    while True:
        time.sleep(1)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                              driver.find_element_by_css_selector(f'div[aria-label="Ergebnisse für {searchTerm}"]'))
        time.sleep(scroll_pause_time)
        new_height = len(driver.find_elements_by_css_selector(f'div[aria-label="Ergebnisse für {searchTerm}"] a'))
        if new_height == last_height:
            break
        last_height = new_height
    return driver


def find_email_from_text(link):
    print('processing: {}'.format(link))
    try:
        res = requests.get(link)
        data = scrapy.Selector(text=res.text)
        data = ' '.join(data.css('::text').extract())
        regex = r'([a-zA-Z0-9._-]+\s?@\s?[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
        emails_found = re.findall(regex, data)
        if len(emails_found) > 0:
            global emails
            emails.extend(emails_found)
    except:
        pass


def find_links(response, website):
    links = response.css('a ::attr(href)').extract()
    domain = website.split('://')[1].split('/')[0]
    links = [v for v in links if domain in v and 'http' in v]
    links.append(website)
    links = list(set(links))
    return links


def find_email(website):
    global emails
    emails = []
    # website = 'https://rixtysoft.com/careers'
    website = 'http://{}'.format(website) if 'http' not in website else website
    res = requests.get(website)
    if res.status_code == 200:
        links = find_links(scrapy.Selector(text=res.text), website)
        threads_list = []
        for link in links:
            newt = Thread(target=find_email_from_text, args=(link,))
            newt.start()
            threads_list.append(newt)
        for t in threads_list:
            t.join()

        emails = list(set([v.strip() for v in emails]))
        return ', '.join(emails)


def insert_to_db(item):
    sql = "INSERT IGNORE INTO google_maps_data (name, address, email, website, telephone, search_term) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (item['name'], item['address'], item['email'], item['website'], item['telephone'], item['search_term'])
    mycursor.execute(sql, val)
    connection.commit()


if __name__ == '__main__':
    browser_locale = 'de'
    connection = mysql.connector.connect(host='dedi1146.your-server.de', database='searcl_db1', user='searcl_1',
                                              password='Gi8jz7RY2sRjESqd')
    mycursor = connection.cursor()
    fileinput = open('googlemapsinput.txt', 'r')
    searchTerms = fileinput.read().split('\n')
    for searchTerm in searchTerms:

        if searchTerm == '':
            continue
        UrlList = []
        url = f'https://www.google.com/maps/search/{searchTerm}/@50.4569511,5.9672567,6z'
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("--lang={}".format(browser_locale))
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        try:
            driver.find_element_by_css_selector(
                'button[aria-label="In die Verwendung von Cookies und anderen Daten zu den beschriebenen Zwecken einwilligen"]').click()
        except:
            pass
        do_scroll(driver)
        for res in driver.find_elements_by_css_selector(f'div[aria-label="Ergebnisse für {searchTerm}"] a'):
            UrlList.append(res.get_attribute('href'))
        for url in UrlList:
            driver.get(url)
            time.sleep(2)
            response = scrapy.Selector(text=driver.page_source)
            item = dict()
            try:
                item['name'] = unidecode.unidecode(response.css('h1 span::text').extract_first(''))
            except:
                item['name']= ''
            try:
                item['address'] = \
                response.css('button[data-item-id="address"] ::attr(aria-label)').extract_first().strip().split(
                    'resse: ')[-1]
                item['address'] = unidecode.unidecode(item['address'])
            except:
                item['address'] = ''
            item['email'] = ''
            try:
                item['website'] = \
                response.css('button[data-tooltip="Website öffnen"] ::attr(aria-label)').extract_first().strip().split(
                    'site: ')[-1]
                if item['website'].strip():
                    item['email'] = find_email(item['website'])
                else:
                    item['email'] = ''
                item['email'] = unidecode.unidecode(item['email'])
            except:
                item['website'] = ''
                item['email'] = ''
            try:
                item['telephone'] = response.css(
                    'button[data-tooltip="Telefonnummer kopieren"] ::attr(aria-label)').extract_first().strip().split(
                    'elefon: ')[-1]

            except:
                item['telephone'] = ''
            try:
                item['search_term'] = unidecode.unidecode(searchTerm)

            except:
                pass
            insert_to_db(item)
            writer.writerow(item)
            fileoutput.flush()
            print('saved: {}'.format(item['name']))
        driver.quit()
