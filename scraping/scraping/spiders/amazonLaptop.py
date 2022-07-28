try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
from threading import Thread
import scrapy
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

csvheaders = ['Product Name', 'price']
file = open('amazonSeller.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, csvheaders)
writer.writeheader()

pgno = 1

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'ubid-main=259-8413721-1705103; session-id=259-4126751-6100162; session-id-apay=259-4126751-6100162; session-id-time=2082787201l; i18n-prefs=USD; s_fid=6A42528A4BF401AD-3FDC049EA62DB5F4; s_vn=1633771150844%26vn%3D1; s_invisit=true; s_cc=true; s_dslv_s=Less%20than%201%20day; aws_lang=en; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1602240468994-920341.38_0; aws-ubid-main=313-5687527-4286463; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A648059270321%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22rixtysoft%22%2C%22keybase%22%3A%22%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; regStatus=registering; s_sq=%5B%5BB%5D%5D; aws-business-metrics-last-visit=1602244257541; s_depth=12; s_dslv=1602245404582; s_nr=1602245404590-Repeat; session-token=RpnQnO0PcN3ELMEH1XI4II8dtiKAFgqh2anqLvqjD/0gmmpwkgJovRHJUTBKlflgeqzVth6iYnhAzmMCGxpehy3Bj2XkqyUbKiY/arDjTJ40FUJgJ43Lf+xe8yTgUMWa8nJgfcL/3szJwNZYGL5TJPpAd5WrF8gH9Kj9JN/J+avrD3BrhkB7q3evpWYrJNn6; csm-hit=tb:DD8RCE9TNSPAPN8QF55F+s-0CVDH40CVHB0Q38MGA6H|1602748081412&t:1602748081412&adb:adblk_yes',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}


def getproducts(url):
    resp = requests.get(url=url, headers=headers)
    response = scrapy.Selector(text=resp.content.decode('utf-8'))
    searchkey=(url.split('3A')[1]).split('&')[0]
    for prod in response.css('.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-12-of-16.sg-col-24-of-28'):
        item = dict()
        item['Product Name'] = prod.css('.a-size-medium.a-color-base.a-text-normal::text').extract_first()
        item['price'] = prod.css('.a-price .a-offscreen::text').extract_first()
        writer.writerow(item)
        file.flush()
    try:
        totalpages = int(response.css('.a-disabled::text').extract()[2])
        # nextpageurl = 'https://www.amazon.com' + response.css('.a-pagination .a-normal a::attr(href)').extract_first()
        # searchKey=(nextpageurl.split('&')[2]).split('3A')[1]
        allpageData(totalpages, searchkey)
    except:
        try:
            totalpages = int(response.css('.a-disabled::text').extract()[2])
            # nextpageurl = 'https://www.amazon.com' + response.css('.a-pagination .a-normal a::attr(href)').extract_first()
            # searchKey = (nextpageurl.split('&')[2]).split('3A')[1]
            allpageData(totalpages, searchkey)
        except:
            print('Quick program ended: ' + searchkey)
            return


def allpageData(totalpages, searchKey):
    pgno = 1
    while pgno <= totalpages:
        pgno = pgno + 1
        url='https://www.amazon.com/s?i=merchant-items&me=A2W496OX3MNYUI&rh=p_4%3A{}&dc&page={}&marketplaceID=ATVPDKIKX0DER&qid=1603697693&ref=sr_pg_{}'.format(searchKey,pgno,pgno)
        resp = requests.get(url=url, headers=headers)
        response = scrapy.Selector(text=resp.content.decode('utf-8'))
        for prod in response.css('.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-12-of-16.sg-col-24-of-28'):
            item2 = dict()
            item2['Product Name'] = prod.css('.a-size-medium.a-color-base.a-text-normal::text').extract_first()
            item2['price'] = prod.css('.a-price .a-offscreen::text').extract_first()
            writer.writerow(item2)
            file.flush()
    print('program ended: '+ searchKey)


if __name__ == '__main__':
    file_ = open('input_amazonsellers.txt', 'r')
    threads = []
    for base_url in file_.read().split('\n'):
        # getproducts(base_url)
        t = Thread(target=getproducts, args=(base_url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    # url='https://www.amazon.com/s?i=merchant-items&me=A2W496OX3MNYUI&rh=p_4%3ABRIGHTFOCAL&dc&marketplaceID=ATVPDKIKX0DER&qid=1602784064&ref=sr_nr_p_4_6'
    # getproducts(url)
