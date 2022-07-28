import csv
import datetime
from urllib.parse import unquote

import requests
import scrapy
from selenium import webdriver

header = ['search term', 'neighborhod', 'url on click', 'machine', 'image', 'under neighborhood name', 'neighborhood description', 'Restaurants', 'Hotels', 'map']
file_out = open('googletravelneighborhood-{}.csv'.format(str(datetime.datetime.now()).replace(':', '-').replace(' ', '_').replace('.', '_')), 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file_out, fieldnames=header)
writer.writeheader()


def parsePage(str_search):
    driver = webdriver.Chrome()
    driver.maximize_window()
    reasons_text = (str_search.replace(',', '+')).replace(' ', '+') + '+neighborhoods'
    url = f'https://www.google.com/search?q={reasons_text}'
    driver.get(url=url)
    neigurls = []
    for href in driver.find_elements_by_css_selector('.mR2gOd .EDblX.DAVP1 a.ct5Ked.klitem-tr.PZPZlf'):
        neigurls.append(href.get_attribute('href'))
    if not neigurls:
        neigurls = [v.find_element_by_class_name('rl_item.rl_item_base').get_attribute('href') for v in driver.find_elements_by_class_name('h998We.mlo-c')]
    for neigurl in neigurls:
        item = dict()
        driver.get(neigurl)
        item['map'] = ''
        try:
            item['map'] = driver.find_element_by_class_name('lu-fs').get_attribute('src')
        except:
            pass
        try:
            item['search term'] = str_search
        except:
            item['search term'] = ''
        try:
            neighborhod = driver.find_element_by_css_selector('.SPZz6b span').text
            neighhod = neighborhod.split()[0]
            item['neighborhod'] = neighborhod
        except:
            neighborhod = ''
            item['neighborhod'] = ''

        item['url on click'] = driver.current_url
        try:
            item['machine'] = '/g/{}'.format([v for v in driver.page_source.split('/g/') if v[0].isdigit()][0].split('\\')[0])
            if len(item['machine']) > 20:
                item['machine'] = '/g/{}'.format([v for v in driver.page_source.split('/g/') if v[0].isdigit()][0].split('&amp;')[0])
                if len(item['machine']) > 20:
                    item['machine'] = '/m/{}'.format([v for v in driver.page_source.split('/m/') if v[0].isdigit()][0].split('\\')[0])
        except:
            try:
                item['machine'] = '/m/{}'.format([v for v in driver.page_source.split('/m/') if v[0].isdigit() if 'SMALL_POLITICALS' in v][0].split('\\')[0])
            except:
                item['machine'] = ''
        # try:
        #     item['machine'] = '/g/' + ([v for v in driver.page_source.split('/g/') if 'LOCATION' in v][0].split(neighborhod)[0].split('\\')[0])
        # except:
        #     try:
        #         item['machine'] = '/m/' + ([v for v in driver.page_source.split('/m/') if 'LOCATION' in v][0].split(neighborhod)[0].split('\\')[0])
        #     except:
        #         item['machine'] = ''
        try:
            item['under neighborhood name'] = driver.find_element_by_css_selector('.wwUB2c.PZPZlf.E75vKf span').text
        except:
            item['under neighborhood name'] = ''
        try:
            item['neighborhood description'] = driver.find_element_by_css_selector('.kno-rdesc span').text
        except:
            item['neighborhood description'] = ''
        try:
            imglink = driver.find_element_by_css_selector('.GMCzAd.BA0A6c img').get_attribute('title')
            if 'wiki' in imglink:
                imgreq = requests.get(imglink)
                imgresp = scrapy.Selector(text=imgreq.content.decode('utf-8'))
                if imgresp.css('.mergedtoprow .image img::attr(src)').extract_first() != None:
                    item['image'] = imgresp.css('.mergedtoprow .image img::attr(src)').extract_first()
                else:
                    item['image'] = imgresp.css('.thumb.tright .image img::attr(src)').extract_first()
            else:
                item['image'] = driver.find_element_by_css_selector('.GMCzAd.BA0A6c img').get_attribute('src')
        except:
            item['image'] = ''

        try:
            item['Restaurants'] = '<p>' + driver.find_element_by_css_selector('div[data-attrid="kc:/location/neighborhood:restaurants"] .LrzXr.kno-fv').get_attribute('innerHTML') + '</p>'
        except:
            item['Restaurants'] = ''

        try:
            item['Hotels'] = '<p>' + driver.find_element_by_css_selector('div[data-attrid="kc:/location/neighborhood:hotels"] .LrzXr.kno-fv').get_attribute('innerHTML') + '</p>'
        except:
            item['Hotels'] = ''
        try:
            driver.find_element_by_css_selector('.GMCzAd.BA0A6c ').click()
            item['image'] = unquote(driver.find_elements_by_class_name('wXeWr.islib.nfEiy.mM5pbd')[0].get_attribute('href'))
            item['image'] = item['image'].split('imgurl=')[1].split('&img')[0]
        except:
            pass
        writer.writerow(item)
        file_out.flush()
    driver.quit()
    return


def getInput():
    fileinput = open('googletravelinput.txt', 'r')
    input_list = fileinput.read()
    return input_list.split('\n')


if __name__ == '__main__':
    inputlist = getInput()
    inputlist = [v for v in inputlist if v.strip()]
    for input in inputlist:
        input = input.replace(', ', ',')
        parsePage(input)
