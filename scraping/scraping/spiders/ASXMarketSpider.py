from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from time import sleep
import scrapy
import os
import urllib.request

file = open('ASXListedCompanies.csv', 'r')
input = file.readlines()[3:]
tickers = []

path = os.getcwd()
csv_header = ['ticker','companyName', 'date-time', 'priceSensitive', 'headline', 'pdfPath']
file = open('asxMarketSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, csv_header)
writer.writeheader()

try:
    p = path + '\PDF'
    os.mkdir(p)
except OSError:
    print("Creation of the directory %s failed" % p)
else:
    print("Successfully created the directory %s " % p)

for inp in input:
    tickers.append(inp.split(',')[1].strip('"'))


def get_dict_value(data, key_list, default=''):
    for key in key_list:
        if data and isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def searchTicker():
    for ticker in tickers:
        try:
            newpath = p + '\{}'.format(ticker)
            os.mkdir(newpath)
        except OSError:
            print("Creation of the directory %s failed" % newpath)
        else:
            print("Successfully created the directory %s " % newpath)


        driver = webdriver.Chrome()
        base_url = 'https://asx.markitdigital.com/test.html?appid=com_asx_markets_announcements'
        try:
            driver.get(base_url)
        except:
            try:
                driver.get(base_url)
            except:
                print('problem with base url')
                return

        sleep(5)
        searchBar = driver.find_element_by_class_name('mk-ac-input')
        sleep(2)
        searchBar.send_keys(ticker)
        sleep(5)
        searchBar.send_keys(Keys.ENTER)
        sleep(5)
        pageSource = driver.page_source
        response = scrapy.Selector(text=pageSource)
        for ls in response.css('#app_container > div > div:nth-child(6) > table > tbody > tr'):
            # #markets_announcements > div > div:nth-child(6) > table > tbody > tr:nth-child(1) > td.text-muted
            item = dict()
            item['ticker']=ticker
            item['companyName'] = ls.css('td:nth-child(4)::text').extract_first().strip()
            date = ls.css('td.text-muted::text').extract_first().strip()
            time = ls.css('td.sr-only::text').extract_first().strip()
            item['date-time'] = '{} - {}'.format(date, time)
            item['priceSensitive'] = ls.css('td.price-sensitive > span::text').extract_first().strip()
            item['headline'] = ls.css('td:nth-child(6) > a::text').extract_first().strip()
            pdflink = ls.css('td:nth-child(6) > a::attr(href)').extract_first()
            urllib.request.urlretrieve(pdflink, "{}/{}.pdf".format(newpath, pdflink.split('/')[-1].split('?')[0]))
            item['pdfPath'] = "{}/{}.pdf".format(newpath, pdflink.split('/')[-1].split('?')[0])
            writer.writerow(item)
            file.flush()

        if (response.css('#app_container > div > div:nth-child(7) > div.col-md-5.col-sm-5.hidden-xs.text-center > ul > li:nth-child(8) > a')):
            nextpage = True
        while nextpage:
            driver.find_element_by_xpath('//*[@id="app_container"]/div/div[5]/div[3]/ul/li[8]/a').click()
            sleep(5)
            pageSource = driver.page_source
            response = scrapy.Selector(text=pageSource)
            for ls in response.css('#app_container > div > div:nth-child(6) > table > tbody > tr'):
                item = dict()
                item['ticker'] = ticker
                item['companyName'] = ls.css('td:nth-child(4)::text').extract_first().strip()
                date = ls.css('td.text-muted::text').extract_first().strip()
                time = ls.css('td.sr-only::text').extract_first().strip()
                item['date-time'] = '{} - {}'.format(date, time)
                item['priceSensitive'] = ls.css('td.price-sensitive > span::text').extract_first().strip()
                item['headline'] = ls.css('td:nth-child(6) > a::text').extract_first().strip()
                pdflink = ls.css('td:nth-child(6) > a::attr(href)').extract_first()
                urllib.request.urlretrieve(pdflink, "{}/{}.pdf".format(newpath, pdflink.split('/')[-1].split('?')[0]))
                item['pdfPath'] = "{}/{}.pdf".format(newpath, pdflink.split('/')[-1].split('?')[0])
                writer.writerow(item)
                file.flush()
            if not response.css('#app_container > div > div:nth-child(7) > div.col-md-5.col-sm-5.hidden-xs.text-center > ul > li:nth-child(8) > a'):
                nextpage = False
            else:
                nextpage = True
        driver.quit()


if __name__ == '__main__':
    searchTicker()
