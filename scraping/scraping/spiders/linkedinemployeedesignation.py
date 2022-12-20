import time
import pandas as pd
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import os
import re
import csv



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
    csvheaders = ['name', 'country', 'location', 'job','public', 'profile link', 'followers','Email']
    csvoutfile = open('linkedinoutputcsv.csv','a+',encoding='utf-8', newline='')
    csvwriter = csv.DictWriter(csvoutfile,fieldnames = csvheaders)
    file_exists = os.path.isfile('linkedinoutputcsv.csv')
    if not file_exists:
        csvwriter.writeheader()
    uniquedesignations = []
    csvread = open('linkedininput.csv', mode='r')
    csvreadfield = ['Keyword', 'Location', 'PagesToScrape', 'LastPageScraped', 'Talk_About']
    csv_reader = csv.DictReader(csvread)


    driver = makebrowserandsignin()
    df = pd.read_csv("linkedininput.csv")
    line_count = 0
    for row in csv_reader:
        driver.get('https://www.linkedin.com/search/results/people/')
        driver.find_element(By.CSS_SELECTOR,'input.search-global-typeahead__input').send_keys(row['Keyword'])
        time.sleep(.5)
        driver.find_element(By.CSS_SELECTOR,'input.search-global-typeahead__input').send_keys(Keys.RETURN)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR,'button[aria-label="Show all filters. Clicking this button displays all available filter options."]').click()
        time.sleep(1)
        for section in driver.find_elements(By.CSS_SELECTOR, '.search-reusables__secondary-filters-filter'):
            if 'Location' in section.find_element(By.CSS_SELECTOR, 'h3').text:
                loc = [v for v in section.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item')[:-1] if
                       row['Location'] in v.find_element(By.CSS_SELECTOR, 'label p span').text]
                if len(loc) < 1:
                    section.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item')[-1].find_element(
                        By.CSS_SELECTOR, 'button').click()
                    time.sleep(2)
                    section.find_element(By.CSS_SELECTOR, 'input[aria-label="Add a location"]').send_keys(
                        row['Location'])
                    time.sleep(2)
                    section.find_element(By.CSS_SELECTOR,
                                         '.basic-typeahead__triggered-content div.basic-typeahead__selectable').click()
                    time.sleep(1)

                else:
                    loc[0].find_element(By.CSS_SELECTOR,'label').click()
                    time.sleep(1)

            if 'Talks about' in section.find_element(By.CSS_SELECTOR, 'h3').text:
                tk_ab = [v for v in section.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item')[:-1] if
                         ('#'+row['Talk_About']) in v.find_element(By.CSS_SELECTOR, 'label p span').text]
                if len(tk_ab) < 1:
                    section.find_elements(By.CSS_SELECTOR, '.search-reusables__filter-value-item')[-1].find_element(
                        By.CSS_SELECTOR, 'button').click()
                    time.sleep(2)
                    section.find_element(By.CSS_SELECTOR, 'input[aria-label="Search a topic"]').send_keys(
                        row['Talk_About'])
                    time.sleep(2)
                    section.find_element(By.CSS_SELECTOR,'.basic-typeahead__triggered-content div.basic-typeahead__selectable').click()
                    time.sleep(1)
                else:
                    tk_ab[0].find_element(By.CSS_SELECTOR,'label').click()
                    time.sleep(1)

        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR,'button[aria-label="Apply current filters to show results"]').click()

        time.sleep(3)
        LastPageScraped = int(row['LastPageScraped'])
        TotalPages = int(row['PagesToScrape'])
        driver.get(driver.current_url+f'&page={LastPageScraped}')
        for i in range(1,TotalPages):
            for member in driver.find_elements(By.CSS_SELECTOR,'.reusable-search__result-container'):
                if 'LinkedIn Member' in member.find_element(By.CSS_SELECTOR,'span.entity-result__title-text a').text:
                    continue
                    # item = dict()
                    # item['name'] = member.find_element(By.CSS_SELECTOR,'span.entity-result__title-text a').text
                    # item['country'] = row['Location']
                    # item['location'] = member.find_element(By.CSS_SELECTOR,'.entity-result__secondary-subtitle').text.strip()
                    # item['job'] = member.find_element(By.CSS_SELECTOR,'.entity-result__primary-subtitle').text.strip()
                    # item['public'] = 'No'
                    # item['profile link'] = 'No'
                    # item['followers'] = 'Unknown'
                    # csvwriter.writerow(item)
                    # csvoutfile.flush()


                else:
                    item = dict()
                    item['name'] = member.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text a').text.split('\n')[0].strip()
                    item['country'] = row['Location']
                    item['location'] = member.find_element(By.CSS_SELECTOR,
                                                           '.entity-result__secondary-subtitle').text.strip()
                    item['job'] = member.find_element(By.CSS_SELECTOR, '.entity-result__primary-subtitle').text.strip()
                    item['public'] = 'Yes'
                    item['profile link'] = member.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text a').get_attribute('href').split('?')[0]
                    try:
                        item['followers'] = member.find_element(By.CSS_SELECTOR, '.entity-result__simple-insight-text-container span').text.strip().split('followers')[0].strip()
                    except:
                        pass
                    driver.execute_script("window.open('');")
                    time.sleep(.5)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(.5)
                    driver.get(item['profile link']+'/overlay/contact-info/')

                    alltext = driver.find_element(By.CSS_SELECTOR,'.pv-profile-section__section-info.section-info').text
                    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', alltext)
                    try:
                        item['Email'] = match[0]
                    except:
                        pass
                    driver.close()
                    time.sleep(.5)
                    driver.switch_to.window(driver.window_handles[0])
                    csvwriter.writerow(item)
                    csvoutfile.flush()

            df.loc[line_count, 'LastPageScraped'] = i+1
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            while True:
                try:
                    driver.find_element(By.CSS_SELECTOR,'button[aria-label="Next"]').click()
                    break
                except:
                    time.sleep(1)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    df.to_csv("linkedininput.csv", index=False)
    driver.quit()