import time

import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

import AirtableApi

basekey = 'appEU3Fjfj6fXA92A'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'obits'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)

processed = []

Links = []


class obitsdeathAirtable(scrapy.Spider):
    name = 'obitsdeathAirtable'

    def start_requests(self):
        options = Options()
        options.add_argument('--headless')
        url = 'http://www.obits.com.au/notices?action=Search+Archives&quick=&state='
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        try:
            driver.find_element_by_css_selector('.navPages > a:nth-child(19)').click()
        except WebDriverException:
            pass
        time.sleep(1)
        while True:
            pg = driver.page_source
            res = scrapy.Selector(text=pg)
            for response in res.css('.noticeResult'):
                link = response.css('h2 a::attr(href)').extract_first()
                Links.append(link)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navPages > a:nth-child(11)")))
            except:
                pass
            try:
                driver.find_element_by_css_selector('.navPages > a:nth-child(11)').click()
            except WebDriverException:
                break
        driver.quit()

        for url in Links:
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        item = dict()
        item['url'] = response.url
        item['Name'] = response.css('.title td::text').extract_first('').strip()
        item['Years of Life'] = response.css('.title th::text').extract_first('').strip()
        if 'Date of Death:' in response.css('.details label')[0].css('::text').extract_first(''):
            item['Date of Death'] = response.css('.details span')[0].css('::text').extract_first('')
            item['Date of Funeral'] = response.css('.details span')[1].css('::text').extract_first('')
            item['Location'] = ' '.join(response.css('.details span')[2].css('::text').extract()).strip().replace('\r\n', ' ')
            item['Time'] = response.css('.details span')[3].css('::text').extract_first('')
        try:
            item['Final Resting Place'] = ''.join(response.css('.other div ::text').extract()).strip().replace('\r\n', ' ')
        except:
            pass
        try:
            item['Funeral Organizer'] = response.css('.contact h3::text').extract_first('').strip()
        except:
            pass
        try:
            item['Funeral Organizer Address'] = response.css('.contact::text').extract()[1].strip() + response.css('.contact::text').extract()[2].strip()
        except:
            pass
        try:
            item['Funeral Organizer Phone'] = response.css('.contact::text').extract()[4].strip()
        except:
            pass
        try:
            if '@' not in response.css('.contact a::text').extract_first(''):
                item['Funeral Organizer Website'] = response.css('.contact a::text').extract_first('')
        except:
            pass

        processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(obitsdeathAirtable)
process.start()
