try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import datetime
import time

import requests
import scrapy
from selenium import webdriver

headers = ['complete', 'Search', 'search', 'url', 'mainpicture url', 'url reason 1', 'reason 1 title',
           'reason 1 description', 'reason 1 mainpicture url', 'url reason 2', 'reason 2 title', 'reason 2 description',
           'reason 2 mainpicture url', 'url reason 3', 'reason 3 title', 'reason 3 description',
           'reason 3 mainpicture url', 'url reason 4', 'reason 4 title', 'reason 4 description',
           'reason 4 mainpicture url', 'url reason 5', 'reason 5 title', 'reason 5 description',
           'reason 5 mainpicture url', 'url reason 6', 'reason 6 title', 'reason 6 description',
           'reason 6 mainpicture url', 'url reason 7', 'reason 7 title', 'reason 7 description',
           'reason 7 mainpicture url', 'url reason 8', 'reason 8 title', 'reason 8 description',
           'reason 8 mainpicture url',
           'TopSite1Title', 'TopSite1url', 'TopSite1text', 'TopSite1TXTurl', 'TopSite2Title', 'TopSite2url',
           'TopSite2text', 'TopSite2TXTurl', 'TopSite3Title', 'TopSite3url', 'TopSite3text', 'TopSite3TXTurl',
           'TopSite4Title', 'TopSite4url', 'TopSite4text', 'TopSite4TXTurl', 'TopSite5Title', 'TopSite5url',
           'TopSite5text', 'TopSite5TXTurl', 'TopSite6Title', 'TopSite6url', 'TopSite6text', 'TopSite6TXTurl',
           'TopSite7Title', 'TopSite7url', 'TopSite7text', 'TopSite7TXTurl', 'TopSite8Title', 'TopSite8url',
           'TopSite8text', 'TopSite8TXTurl', 'TopExperience1Title', 'TopExperience1imgurl', 'TopExperience1txt',
           'TopExperience1link', 'TopExperience2Title', 'TopExperience2imgurl', 'TopExperience2txt',
           'TopExperience2link', 'TopExperience3Title', 'TopExperience3imgurl', 'TopExperience3txt',
           'TopExperience3link', 'TopExperience4Title', 'TopExperience4imgurl', 'TopExperience4txt',
           'TopExperience4link', 'TopExperience5Title', 'TopExperience5imgurl', 'TopExperience5txt',
           'TopExperience5link', 'TopExperience6Title', 'TopExperience6imgurl', 'TopExperience6txt',
           'TopExperience5link', 'Neigh1title', 'Neigh1url', 'Neigh1imgurl', 'Neigh1txt', 'Neigh2title', 'Neigh2url', 'Neigh2imgurl', 'Neigh2txt', 'Neigh3title', 'Neigh3url', 'Neigh3imgurl', 'Neigh3txt',
           'Neigh4title', 'Neigh4url', 'Neigh4imgurl', 'Neigh4txt', 'Neigh5title', 'Neigh5url', 'Neigh5imgurl', 'Neigh5txt', 'TravelArticle1Title', 'TravelArticle1url',
           'TravelArt1imageurl', 'TravelArticle2Title', 'TravelArticle2url', 'TravelArt2imageurl',
           'TravelArticle3Title', 'TravelArticle3url', 'TravelArt3imageurl', 'TravelArticle4Title', 'TravelArticle4url',
           'TravelArt4imageurl', 'TravelArticle5Title', 'TravelArticle5url', 'TravelArt5imageurl']

fileout = open('googletravel-{}.csv'.format(str(datetime.datetime.now()).replace(':', '-').replace(' ', '_').replace('.', '_')), 'w', encoding='utf-8', newline='')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


def parsePage(str_search):
    url = 'https://www.google.com/travel/'
    driver.get(url=url)
    reasons_text = str_search.split(',')[0]
    driver.find_element_by_xpath(
        '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/div/div[1]/div[1]/div[2]/c-wiz/div/div/div/div/div[1]/div[1]/input').send_keys(
        reasons_text)
    time.sleep(3)
    ps = driver.page_source
    responce = scrapy.Selector(text=ps)
    for dri in responce.css('.sbsb_c'):
        if str_search.split(',')[1] in dri.css('.MS0IOc.L7lLnb::text').extract_first(''):
            id = dri.css('.JmIFMd::attr(id)').extract_first()
            break
    try:
        driver.find_element_by_id(f'{id}').click()
    except:
        driver.find_element_by_id('sbse0').click()
    time.sleep(5)
    ps = driver.page_source
    responce = scrapy.Selector(text=ps)
    item = dict()
    item['Search'] = str_search
    item['search'] = str_search.split(',')[0]

    item['url'] = driver.current_url
    mainurl = driver.current_url
    try:
        item['mainpicture url'] = driver.find_element_by_xpath(
            '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div/div[1]/div[2]/c-wiz/div/div[1]/div/div/easy-img/img').get_attribute(
            'src')
    except:
        return
        # parsePage(str_search)
        # return
    city_title = ' '.join([v.capitalize() for v in reasons_text.split() if v.strip()])
    for i, resp in enumerate(
            responce.css(f'div[aria-label="Reasons to visit {city_title}"] .NmNuT.FsHM4e')):
        if i >= 8:
            break
        item[f'url reason {i + 1}'] = 'https://www.google.com' + resp.css('a::attr(href)').extract_first()
        url = 'https://www.google.com' + resp.css('a.Ld2paf::attr(href)').extract_first()
        driver.get(url=url)
        ps = driver.page_source
        responce1 = scrapy.Selector(text=ps)
        item[f'reason {i + 1} title'] = responce1.xpath(
            '/html/body/c-wiz[2]/div/div/div/div[3]/div/div[2]/text()').extract_first()
        try:
            driver.find_element_by_css_selector('.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.ksBjEc.lKxP2d').click()
            item[f'reason {i + 1} description'] = driver.find_element_by_class_name(
                'GmvXSb').text + ' ' + driver.find_element_by_css_selector('.GmvXSb.qDLGm').text
            item[f'reason {i + 1} mainpicture url'] = driver.find_element_by_css_selector(
                '.R1Ybne.YH2pd').get_attribute('src')
        except:
            item[f'reason {i + 1} description'] = ''
            item[f'reason {i + 1} mainpicture url'] = ''
    driver.get(url=mainurl)
    for i, resp in enumerate(driver.find_elements_by_css_selector('div[aria-label="Top sights"] .f4hh3d')):
        if i >= 8:
            break
        resp.click()
        time.sleep(5)
        try:
            item[f'TopSite{i + 1}Title'] = driver.find_element_by_css_selector('.HVJNrc.jr5G9b.enpmuc').text
        except:
            item[f'TopSite{i + 1}Title'] = ''
        try:
            imglist = []
            for img in driver.find_elements_by_css_selector('.dBuxib.rmbpBd'):
                if img.find_element_by_tag_name('img').get_attribute('src'):
                    imglist.append(img.find_element_by_tag_name('img').get_attribute('src'))
                else:
                    imglist.append(img.find_element_by_tag_name('img').get_attribute('data-src'))
            item[f'TopSite{i + 1}url'] = ' || '.join(imglist)
        except:
            item[f'TopSite{i + 1}url'] = ''
        try:
            item[f'TopSite{i + 1}text'] = driver.find_element_by_css_selector('.NYYuTb').text
        except:
            item[f'TopSite{i + 1}text'] = ''
        try:
            item[f'TopSite{i + 1}TXTurl'] = driver.find_element_by_css_selector('.NYYuTb').find_element_by_tag_name(
                'a').get_attribute('href')
        except:
            item[f'TopSite{i + 1}TXTurl'] = ''

    for i, rep in enumerate(
            driver.find_elements_by_css_selector('div[aria-label="Top experiences"] .fCQNhc.iwwqZc.oBMSEc')):
        if i >= 7:
            break
        try:
            item[f'TopExperience{i + 1}Title'] = rep.find_element_by_css_selector('.skFvHc.YmWhbc').text
        except:
            item[f'TopExperience{i + 1}Title'] = ''
        time.sleep(3)
        try:
            item[f'TopExperience{i + 1}imgurl'] = rep.find_element_by_css_selector('.kXlUEb img').get_attribute('src')
        except:
            item[f'TopExperience{i + 1}imgurl'] = ''
        try:
            item[f'TopExperience{i + 1}txt'] = rep.find_element_by_css_selector('.nFoFM').text
        except:
            item[f'TopExperience{i + 1}txt'] = ''
        try:
            item[f'TopExperience{i + 1}link'] = 'https://www.google.com' + rep.find_element_by_css_selector('.Ld2paf').get_attribute(
                'data-href')
        except:
            item[f'TopExperience{i + 1}link'] = ''

    for i, rept in enumerate(driver.find_elements_by_css_selector('div[aria-label="Travel articles"] .NmNuT')):
        if i >= 5:
            break
        try:
            item[f'TravelArticle{i + 1}Title'] = rept.find_element_by_css_selector('.rbj0Ud .skFvHc').text
        except:
            item[f'TravelArticle{i + 1}Title'] = ''
        try:
            item[f'TravelArticle{i + 1}url'] = rept.find_element_by_css_selector(
                '.NnEw9.OBk50c.DkSkOd.ErXY2c a').get_attribute('href')
        except:
            item[f'TravelArticle{i + 1}url'] = ''
        try:
            item[f'TravelArt{i + 1}imageurl'] = rept.find_element_by_css_selector('img.R1Ybne.YH2pd').get_attribute('data-src')
        except:
            item[f'TravelArt{i + 1}imageurl'] = ''
    srcs = []
    for i, respt in enumerate(
            driver.find_elements_by_css_selector('div[aria-label="Notable neighborhoods"] .NmNuT')):
        if i >= 5:
            break
        try:
            item[f'Neigh{i + 1}title'] = respt.find_element_by_css_selector('.xWLMD.P0n0Vb .d2vL5e').text
        except:
            item[f'Neigh{i + 1}title'] = ''
        try:
            item[f'Neigh{i + 1}url'] = respt.find_element_by_css_selector('.NnEw9.OBk50c.DkSkOd.xoPjAc.jGm8fb a').get_attribute('href')
            link = respt.find_element_by_css_selector('.NnEw9.OBk50c.DkSkOd.xoPjAc.jGm8fb a').get_attribute('href')
            try:
                response = requests.get(url=link)
                resp = scrapy.Selector(text=response.text)
                item[f'Neigh{i + 1}txt'] = resp.css('.BNeawe.s3v9rd.AP7Wnd::text').extract_first()
            except:
                item[f'Neigh{i + 1}txt'] = ''
        except:
            item[f'Neigh{i + 1}url'] = ''
        srcs.append(respt.find_element_by_css_selector('.Ld2paf.w5wyid').get_attribute('href'))

    for i, src in enumerate(srcs):
        driver.get(src)
        try:
            item[f'Neigh{i + 1}imgurl'] = driver.find_element_by_css_selector('.umyQi .rISBZc.M4dUYb').get_attribute('src')
        except:
            item[f'Neigh{i + 1}imgurl'] = ''

    writer.writerow(item)
    fileout.flush()
    return


def getInput():
    fileinput = open('googletravelinput.txt', 'r')
    input_list = fileinput.read()
    return input_list.split('\n')


if __name__ == '__main__':
    inputlist = getInput()

    driver = webdriver.Chrome()
    inputlist = [v for v in inputlist if v.strip()]
    for input in inputlist:
        parsePage(input)
    driver.quit()
