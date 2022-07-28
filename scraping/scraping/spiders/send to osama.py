from selenium import webdriver
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from time import sleep
import csv
import pandas as pd

connection_timeout = 30  # seconds

url_en = 'https://www.brandrange.com/us/en/men/shoes/sneakers.html'

options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)
driver.get(url_en)

soup = BeautifulSoup(driver.page_source, 'html.parser')

ar_link = soup.find('header', {'class': 'header header6'}).find('div', {'class': 'top-header-content'}).find('div', {'class': 'left-top-content'}).find('div', {'class': 'switcher currency switcher-currency'}).find_all('div')
ar_link1 = ar_link[0].find('div', {'class': 'ui-dialog ui-widget ui-widget-content ui-corner-all ui-front mage-dropdown-dialog'})
print(ar_link1.find_all('a')[0].get('href'))
driver.get(ar_link1.find_all('a')[0].get('href'))
driver.find_element_by_id('account-actions-language').click()
record_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True
prod_list = []
to_csv = []

while scrolling:
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # this line of code neded to be inside the loop
    prod = soup.find_all('div', {'class', 'product-item-info'})

    for item in prod[-12:]:
        href = item.find('div', {'class': 'product-detail-content'}).find('a').get('href')
        name = item.find('div', {'class': 'product-detail-content'}).find('a').text
        desc = item.find('div', {'class': 'product-detail-content'}).find('h6').find('a').text

        if [href, name, desc] not in prod_list:
            prod_list.append([href, name, desc])
            to_csv.append([href, name, desc])
            # csvwriter.writerow({'href':href,'name':name,'desc':desc}) #CSV writing code
            # filecsven.flush() #CSV writing code

    scroll_attempt = 0

    print(len(prod_list))

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1

            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = curr_position
            break

        # print(prod_list)
# print(len(prod_list))
pd.DataFrame(to_csv).to_csv('eng_output.csv')
