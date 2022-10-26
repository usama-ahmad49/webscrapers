import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By

# import common


STAT_FILE = 'linkedin.stat'
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

def parse_ind_profile(driver,link):
    if link not in crawled:
        driver.execute_script("window.open('');")

        # Switch to the new window and open new URL
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        Selector_ind_profile = scrapy.Selector(text=driver.page_source)
        item = dict()
        item['url'] = driver.current_url
        item['name'] = Selector_ind_profile.css('h1::text').extract_first()
        item['profession'] = Selector_ind_profile.css('div.text-body-medium.break-words::text').extract_first().strip()
        item['location'] = Selector_ind_profile.css('span.text-body-small.inline.t-black--light.break-words::text').extract_first().strip()
        item['company'] = Selector_ind_profile.css('span.text-body-small.inline.t-black--light.break-words::text').extract_first().strip()
        driver.get(driver.current_url+'/details/experience/')
        Selector_experiance = scrapy.Selector(text=driver.page_source)
        item['institution'] = ', '.join([v.split('logo')[0].strip() for v in Selector_experiance.css('.ivm-view-attr__img--centered.EntityPhoto-square-3.lazy-image.ember-view::attr(alt)').extract()])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        crawled.add(item['url'])

        profile = common.Profile(
            name=item.get('name'), profession=item.get('profession'),
            company = item.get('company'),institution=item.get('institution'),
            location=item.get('location'),url=item.get('url')
        )
        return profile
    else:
        return None


def parse_profiles_page(driver):
    Selector = scrapy.Selector(text=driver.page_source)
    for sel in Selector.css('.reusable-search__result-container'):
        link = sel.css('a::attr(href)').extract_first()
        name = ''.join(sel.css('a::text').extract()).strip()
        if 'LinkedIn Member' != name:
            profile = parse_ind_profile(driver, link)
            if profile:
                common.to_thunderstorm([profile], 'linkedin')


if __name__ == '__main__':
    crawled = common.load_crawled(STAT_FILE)

    fileinput = open('linkedincompaniescrawl.txt','r')
    companynames = fileinput.read().split('\n')
    driver = makebrowserandsignin()
    for companyname in companynames:
        driver.get('https://www.linkedin.com/search/results/people/')
        driver.find_element(By.CSS_SELECTOR,'button[aria-label="Current company filter. Clicking this button displays all Current company filter options."]').click()
        driver.find_element(By.CSS_SELECTOR,'input[aria-label="Add a company"]').click()
        driver.find_element(By.CSS_SELECTOR,'input[aria-label="Add a company"]').send_keys(companyname)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,'.basic-typeahead__selectable').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,'#hoverable-outlet-current-company-filter-value button[aria-label="Apply current filter to show results"]').click()
        link = driver.current_url
        for i in range(1,101):
            url = link.split('&page')[0]+f'&page={i}'
            driver.get(url)
            parse_profiles_page(driver)
    common.update_crawled(crawled, STAT_FILE)
    driver.quit()