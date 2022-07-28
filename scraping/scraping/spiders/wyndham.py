import logging
import time
from datetime import datetime

import scrapy
from selenium import webdriver

import AirtableApi

Processed = []
table_name = 'wyndham'
basekey = 'appF5JU1xjzYCHQLL'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'
airtable_client = AirtableApi.AirtableClient(apikey, basekey)

if __name__ == '__main__':
    url = 'https://eproperty.wyndham.vic.gov.au/ePropertyPROD/P1/eTrack/eTrackApplicationSearch.aspx?r=P1.WEBGUEST&f=P1.ETR.SEARCH.ENQ'
    driver = webdriver.Firefox()
    driver.get(url)
    now = datetime.today()
    now = datetime.strftime(now, '%d-%b-%Y')
    driver.find_element_by_css_selector('#ctl00_Content_txtDateFrom input').send_keys('1-jan-1960')
    time.sleep(0.5)
    driver.find_element_by_css_selector('#ctl00_Content_txtDateTo input').send_keys(now)
    time.sleep(0.5)
    driver.find_element_by_id('ctl00_Content_btnSearch').click()
    page = 1
    iterator = 0
    while True:
        logging.warning(f"Page no. {page}")
        response = scrapy.Selector(text=driver.page_source)
        for res in response.css('#ctl00_Content_cusResultsGrid_pnlCustomisationGrid .normalRow, .alternateRow'):
            item = dict()
            item['Application ID'] = res.css('td:nth-child(1) a::text').extract_first('')
            item['Date Received'] = res.css('td:nth-child(2) ::text').extract_first('')
            item['Description'] = res.css('td:nth-child(3) ::text').extract_first('')
            item['Address'] = res.css('td:nth-child(4) ::text').extract_first('')
            item['Status'] = res.css('td:nth-child(5) ::text').extract_first('')
            item['Decision'] = res.css('td:nth-child(6) ::text').extract_first('')
            item['Ward'] = res.css('td:nth-child(7) ::text').extract_first('')
            item['Estimated Cost'] = res.css('td:nth-child(8) ::text').extract_first('')
            item['Objections Received'] = res.css('td:nth-child(9) ::text').extract_first('')
            Processed.append(item)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page += 1
        iterator += 1
        try:
            if str(page) in driver.find_elements_by_css_selector('.pagerRow table td')[iterator].text:
                driver.find_elements_by_css_selector('.pagerRow table td')[iterator].click()
                time.sleep(0.5)
            elif '...' in driver.find_elements_by_css_selector('.pagerRow table td')[iterator].text:
                driver.find_elements_by_css_selector('.pagerRow table td')[iterator].click()
                time.sleep(2)
                if '...' in driver.find_elements_by_css_selector('.pagerRow table td')[-1].text:
                    iterator = 1
                else:
                    lastpage = int(driver.find_elements_by_css_selector('.pagerRow table td')[-1].text)
                    rempage = lastpage - 10
                    iterator = (10 - rempage) + 1
        except:
            break

    driver.quit()
    firstcol = 'Application ID'
    airtable_client.insert_records(table_name, Processed, firstcol)
    print('Done')
