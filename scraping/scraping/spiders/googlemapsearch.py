from seleniumwire import webdriver
import scrapy
from selenium.webdriver.common.keys import Keys
import time
import csv

header=['name','website','address']
file = open('googlemapsearch.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()

file_urls=open('url_google_bussiness.txt','w')

def managebusiness(driver):
    links=driver.find_elements_by_css_selector('.rlfl__tls.rl_tls .VkpGBb')
    for link in links:
        link.click()
        time.sleep(5)
        for ownbus in driver.find_elements_by_css_selector('.SOGtLd.duf-h a'):
            if 'Own this business?' in ownbus.text:
                file_urls.write(ownbus.get_attribute('href'))
                file_urls.write("\n")
                file_urls.flush()
def parsedata(driver):
    ps = driver.page_source
    response = scrapy.Selector(text=ps)
    for resp in response.css('.rlfl__tls.rl_tls .VkpGBb'):
        item=dict()
        if resp.css('a.yYlJEf.L48Cpd'):
            item['website']=resp.css('a.yYlJEf.L48Cpd::attr(href)').extract_first()
        item['address'] = resp.css('.rllt__details.lqhpac div')[1].css('span ::text').extract_first()
        item['name'] = resp.css('.dbg0pd ::text').extract_first()
        writer.writerow(item)
        file.flush()

if __name__ == '__main__':
    driver= webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.google.com/')
    driver.find_element_by_css_selector('input[title="Search"]').send_keys('plumber in maryland')
    time.sleep(1)
    driver.find_element_by_css_selector('input[title="Search"]').send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_element_by_css_selector('.Q2MMlc').click()
    time.sleep(3)
    while True:
        parsedata(driver)
        managebusiness(driver)
        webdriver.ActionChains(driver).move_to_element(driver.find_element_by_css_selector('#pnnext')).perform()
        if driver.find_element_by_css_selector('#pnnext'):
            driver.find_element_by_css_selector('#pnnext').click()
            time.sleep(3)
        else:
            file_urls.close()
            break



