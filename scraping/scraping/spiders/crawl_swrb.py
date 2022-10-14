import time

import requests
import scrapy
from selenium import webdriver
from scrapy.crawler import CrawlerProcess
import common
# from common import get_index
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def get_driver():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def extract_profile(selector, link):
    item = dict()
    IDPART = [v for v in selector.css('td::attr(id)').extract() if '36iT0R0x0' in v][0].split('36iT0R0x0')[0]
    item['name'] = selector.css("#" + IDPART + "36iT0R0x0 div::text").extract_first('').strip() + ' ' + \
                   selector.css("#" + IDPART + "45iT0R0x0 div::text").extract_first('').strip()
    item['reg_no'] = selector.css("#" + IDPART + "27iT0R0x0 div::text").extract_first('').strip()
    item['gender'] = selector.css("#" + IDPART + "63iT0R0x0 div::text").extract_first('').strip()
    item['company'] = selector.css("#" + IDPART + "72iT0R0x0 div::text").extract_first('').strip()
    item['reg_type'] = selector.css("#" + IDPART + "81iT0R0x0 div::text").extract_first('').strip()
    item['url'] = link
    item['practicing_certificate'] = selector.css("#" + IDPART + "135iT0R0x0 div::text").extract_first('').strip()
    return item


def parse_profile(driver, url):
    if url not in crawled:
        crawled.add(url)
        driver.get(url)
        selector = scrapy.Selector(text=driver.page_source)
        item = extract_profile(selector, url)

        profile = common.Profile(
            name=item['name'], profession='Rehabilitation Counsellor', company=item['company'], reg_no=item['reg_no'],
            url=item['url'],
            reg_type=item['reg_type'], gender=item['gender'], practicing_certificate=item['practicing_certificate']
        )

        return profile
    else:
        return None


if __name__ == '__main__':
    STAT_FILE = 'swrb.stat'
    NAME = 'swrb'
    crawled = common.load_crawled(STAT_FILE)
    driver = get_driver()

    driver.get('https://my.swrb.govt.nz/_Web/Public/Public-Register.aspx')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    time.sleep(5)
    element = driver.find_element(By.ID, "ste_container_ciNewContentHtml3_2962f0666c3749dea95910a0fbe09183")

    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    driver.find_element(By.CSS_SELECTOR,
                        '#ctl00_TemplateBody_WebPartManager1_gwpciSearchregister_ciSearchregister_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Arrow').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#ctl00_TemplateBody_WebPartManager1_gwpciSearchregister_ciSearchregister_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_listbox > li:nth-child(3)').click()
    time.sleep(5)
    TotalPages = int(driver.find_element(By.CSS_SELECTOR,
                                         '#ctl00_TemplateBody_WebPartManager1_gwpciSearchregister_ciSearchregister_ResultsGrid_Grid1_ctl00 > tfoot > tr > td > table > tbody > tr > td > div.rgWrap.rgInfoPart > strong:nth-child(2)').text.strip())
    AllElemOnPage = driver.find_elements(By.CSS_SELECTOR,
                                         '#ctl00_TemplateBody_WebPartManager1_gwpciSearchregister_ciSearchregister_ResultsGrid_Grid1_ctl00 > tbody tr td a')
    UrlList = []
    for elem in AllElemOnPage:
        UrlList.append(elem.get_attribute('href'))

    for i in range(0, TotalPages):
        driver.find_element(By.CSS_SELECTOR, 'input.rgPageNext').click()
        time.sleep(5)
        AllElemOnPage = driver.find_elements(By.CSS_SELECTOR,
                                             '#ctl00_TemplateBody_WebPartManager1_gwpciSearchregister_ciSearchregister_ResultsGrid_Grid1_ctl00 > tbody tr td a')

        profile_driver = get_driver()
        for elem in AllElemOnPage:
            profile = parse_profile(driver=profile_driver, url=elem.get_attribute('href'))
            if profile:
                common.to_thunderstorm([profile], 'swrb')
            # UrlList.append(elem.get_attribute('href'))
        profile_driver.close()

    common.update_crawled(crawled, STAT_FILE)
    driver.quit()
