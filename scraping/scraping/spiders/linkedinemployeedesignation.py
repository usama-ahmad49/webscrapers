import time

import requests
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By

import urllib.request
import os
import csv
cwd = os.getcwd()


# value = open('proxies.txt','r')
# proxy = value.readlines()[0]
#
# certificate = os.path.join(cwd, 'zyte-smartproxy-ca.crt')
# proxy_auth = proxy
# proxies={
#         "http": f"http://{proxy_auth}@proxy.crawlera.com:8011/",
#         "https": f"http://{proxy_auth}@proxy.crawlera.com:8011/",
#     }
def set_http_proxy(proxy):
        if proxy == None: # Use system default setting
            proxy_support = urllib.request.ProxyHandler()
        elif proxy == '': # Don't use any proxy
            proxy_support = urllib.request.ProxyHandler({})
        else: # Use proxy
            proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)


def makebrowserandsignin():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1880,1300")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.linkedin.com/login')
    # driver.find_element(By.CSS_SELECTOR,'#username').send_keys('usamaahmed2222@gmail.com')
    driver.find_element(By.CSS_SELECTOR,'#username').send_keys('rixtysoft01@gmail.com')
    # driver.find_element(By.CSS_SELECTOR,'#password').send_keys('M@nzoor007')
    driver.find_element(By.CSS_SELECTOR,'#password').send_keys('qwerty123uiop')
    driver.find_element(By.CSS_SELECTOR,'button[data-litms-control-urn="login-submit"]').click()

    return driver

# def getgooglelinks(filedesignations):
#     for des in filedesignations:
#         if des != '':
#             url = f'https://www.google.com/search?q=site:linkedin.com {companyname} intitle"{des}"&sxsrf=ALiCzsZ0Q9wAg43iYoRf35wNpTjxpCJtGw:1666909552823&ei=cAVbY6XnMf7cptQPzu2pgAk&ved=0ahUKEwil35L-uYH7AhV-rokEHc52CpAQ4dUDCA8&uact=5&oq=site:linkedin.com {companyname} intitle"{des}"&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGAFKBAhGGABQ6RdY6RdghCVoAnAAeACAAZ0BiAGdAZIBAzAuMZgBAKABAqABAcABAQ&sclient=gws-wiz&num=100'
#
#             response = requests.get(url, proxies=proxies, verify=certificate)
#             googleselector = scrapy.Selector(text=response.text)
#             googlelinklist = googleselector.css('.kvH3mc.BToiNc.UK95Uc a::attr(href)').extract()
#             with open('googlelinklist.txt','a+') as gll:
#                 for gl in googlelinklist:
#                     if gl != '#':
#                         gll.write(gl+'\n')


def parse_profiles_page(driver):
    Selector = scrapy.Selector(text=driver.page_source)
    for sel in Selector.css('.reusable-search__result-container'):
        link = sel.css('a::attr(href)').extract_first()
        designationfull = ''.join(sel.css('.entity-result__primary-subtitle.t-14.t-black.t-normal::text').extract()).strip()
        if 'at' in designationfull:
            designation = designationfull.split('at')[0].strip()
            uniquedesignations.append(designation)

        # if 'LinkedIn Member' != name:
        # parse_ind_profile(driver, link)


if __name__ == '__main__':
    uniquedesignations = []
    csvread = open('linkedininput.csv', mode='r')
    csv_reader = csv.DictReader(csvread)

    # fileinput = open('inputlinkedin.csv','r', encoding='utf-8')
    # companynames = fileinput.read().split('\n')
    driver = makebrowserandsignin()
    line_count = 0
    for row in csv_reader:
        # if line_count == 0:
        #     print(f'Column names are {", ".join(row)}')
        #     line_count += 1
        #     continue
        driver.get('https://www.linkedin.com/search/results/people/')
        driver.find_element(By.CSS_SELECTOR,'button[aria-label="Show all filters. Clicking this button displays all available filter options."]').click()
        time.sleep(1)
        # driver.find_element(By.CSS_SELECTOR,'input[aria-label="Add a company"]').click()
        # driver.find_element(By.CSS_SELECTOR,'input[aria-label="Add a company"]').send_keys(row['Keyword'])
        # time.sleep(2)
        # driver.find_element(By.CSS_SELECTOR,'.basic-typeahead__selectable').click()
        # time.sleep(2)
        # driver.find_element(By.CSS_SELECTOR,'#hoverable-outlet-current-company-filter-value button[aria-label="Apply current filter to show results"]').click()
        time.sleep(2)

        for section in driver.find_elements(By.CSS_SELECTOR, '.search-reusables__secondary-filters-filter'):
            if 'Location' in section.find_element(By.CSS_SELECTOR, 'h3').text:
                loc = [v for v in driver.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item') if
                       row['Location'] in v.find_element(By.CSS_SELECTOR, 'label p span').text]
                if len(loc) < 1:
                    driver.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item')[-1].find_element(
                        By.CSS_SELECTOR, 'button').click()
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Add a location"]').send_keys(
                        row['Location'])
                    time.sleep(.5)
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Add a location"]')

        totalresults = int(driver.find_element(By.CSS_SELECTOR,'.search-results-container h2').text.split(' ')[0].replace(',',''))
        pages = totalresults/10
        pages = int(pages)+1
        if pages>101:
            pages = 101
        link = driver.current_url
        for i in range(1,pages):
            if i == 1:
                url = link
            else:
                url = link.split('&page')[0] + f'&page={i}'
            driver.get(url)
            parse_profiles_page(driver)
        uniquedesignations = list(set(uniquedesignations))
        with open('linkedindesignations.txt','w') as ld:
            for u in uniquedesignations:
                try:
                    ld.write(u.encode('utf-8')+'\n')
                except:
                    pass

    driver.quit()
    # with open('linkedindesignations.txt','r') as ldr:
    #     filedesignations = ldr.read().split('\n')
    # getgooglelinks(filedesignations)
