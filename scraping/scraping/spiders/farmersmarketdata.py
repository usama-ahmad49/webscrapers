import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
headers=['Facebook','Twitter','Instagram']
fileout = open('farmersmarketdata.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(fileout,fieldnames=headers)
writer.writeheader()
def datasave(list):
    item=dict()
    item['Facebook']=list[0]
    item['Twitter']=list[1]
    item['Instagram']=list[2]
    writer.writerow(item)
    fileout.flush()


def googlesearchlink(str):
    links=[]
    driver = webdriver.Chrome()
    link = f"https://www.google.com/search?q={str}"
    driver.get(link)
    url=''
    for result in driver.find_elements_by_css_selector('#rso .g'):
        url = result.find_element_by_css_selector('.yuRUbf a').get_attribute('href')
        if 'facebook.com' in url or 'yelp.com' in url or 'patch.com' in url:
            continue
        else:
            break
    driver.set_page_load_timeout(5)
    try:
        driver.get(url)
    except:
        pass
    ps = driver.page_source
    if 'facebook.com/' in ps:
        facebooklink = f"https://www.facebook.com/{ps.split('facebook.com/')[1].split('/')[0]}/"
    else:
        facebooklink = ''
    links.append(facebooklink.split(' ')[0].split('"')[0])
    if 'twitter.com/' in ps:
        twitterlink = f"https://www.twitter.com/{ps.split('twitter.com/')[1].split('/')[0]}/"
    else:
        twitterlink = ''
    links.append(twitterlink.split(' ')[0].split('"')[0])
    if 'instagram.com/' in ps:
        instagramlink = f"https://www.instagram.com/{ps.split('instagram.com/')[1].split('/')[0]}/"
    else:
        instagramlink = ''
    driver.close()
    links.append(instagramlink.split(' ')[0].split('"')[0])
    return links



def checkweblink(link):
    links = []
    link = f'https://www.{link}'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(5)
    try:
        driver.get(link)
    except:
        pass
    ps = driver.page_source
    if 'facebook.com/' in ps:
        facebooklink = f"https://www.facebook.com/{ps.split('facebook.com/')[1].split('/')[0]}/"
    else:
        facebooklink = ''
    links.append(facebooklink.split(' ')[0].split('"')[0])
    if 'twitter.com/' in ps:
        twitterlink = f"https://www.twitter.com/{ps.split('twitter.com/')[1].split('/')[0]}/"
    else:
        twitterlink = ''
    links.append(twitterlink.split(' ')[0].split('"')[0])
    if 'instagram.com/' in ps:
        instagramlink = f"https://www.instagram.com/{ps.split('instagram.com/')[1].split('/')[0]}/"
    else:
        instagramlink = ''
    driver.close()
    links.append(instagramlink.split(' ')[0].split('"')[0])
    return links


if __name__ == '__main__':
    df = pd.read_excel('Farmers Market Data Test.xlsx', 'Farmers Markets',header=[0,1])
    for i, weblink in enumerate(df['Links']['Website']):
        if isinstance(weblink, str):
            links = checkweblink(weblink)
            datasave(links)
        else:
            name = df['Unnamed: 0_level_0']['Name'][i]
            links = googlesearchlink(name)
            datasave(links)
