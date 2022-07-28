import csv
import time
from seleniumwire import webdriver
from datetime import datetime
from threading import Thread

import requests
import scrapy

file_headers = ['Record_No.', 'Link', 'Breadcrumbs', 'Chemical Name', 'Synonyms', 'CAS No.', 'Molecular Formula', 'MDL Number', 'HS Code', 'Presursor', 'Product']
fileOut = open('molbase2.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileOut, fieldnames=file_headers)
writer.writeheader()

proxies_dict = {
    'https': "https://{}:{}".format('142.54.161.98', '19004'),
    'http': "http://{}:{}".format('142.54.161.98', '19004')
}
count = 0


def make_request(url):
    got = False
    while not got:
        try:
            resp = requests.get(url, proxies=proxies_dict, headers=headers, allow_redirects=False)
            if resp.status_code == 200 and resp.url != 'http://key.molbase.com':
                got = True
            else:
                print(resp.status_code)
                time.sleep(1)
        except Exception as e:
            print(str(e))
    return resp


def parse_ind_data(resp_raw, new_url_cat):
    response = scrapy.Selector(text=resp_raw.content.decode('utf-8'))
    item = dict()
    global count
    count = count + 1
    item['Record_No.'] = count
    item['Link'] = new_url_cat
    try:
        item['Breadcrumbs'] = ''.join(response.css('.crumbs ::text').extract()).replace('\n', '').replace(' ','').replace(' ', '').replace('>',' > ')
    except:
        pass
    try:
        item['Chemical Name'] = response.css('a.cpd-name ::text').extract_first()
    except:
        pass
    try:
        item['Synonyms'] = '|||'.join(response.css('#basic .en-list a.synonyms::text').extract())
    except:
        pass
    try:
        item['CAS No.'] = response.css('.bk-head dd .col em span::text').extract()[0]
    except:
        pass
    try:
        item['Molecular Formula'] = response.css('.bk-head dd .col em span::text').extract()[1]
    except:
        pass
    try:
        for MDL in response.css('#number tr'):
            if 'MDL' in MDL.css('th::text').extract_first():
                item['MDL Number'] = MDL.css('td::text').extract_first()
                break
    except:
        item['MDL Number'] = ''
    try:
        for HS in response.css('#safe tr'):
            if 'HS Code' in HS.css('th::text').extract_first():
                item['HS Code'] = HS.css('td::text').extract_first()
                break
    except:
        item['HS Code'] = ''
    try:
        item['Presursor'] = '|||'.join(response.css('#precursor dl dd a p::text').extract())
    except:
        pass
    try:
        item['Product'] = '|||'.join(response.css('#downstream dl dd a p::text').extract())
    except:
        pass
    writer.writerow(item)
    fileOut.flush()
    print('record recieved: ' + resp_raw.url)


def parse(resp_raw, new_url):
    urlList = []
    response = scrapy.Selector(text=resp_raw.content.decode('utf-8'))
    for elem in response.css('.s-list li'):
        link = elem.css('a::attr(href)').extract_first()
        url = f'http://www.molbase.com{link}'
        urlList.append(url)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    for url in urlList:
        resp3 = make_request(url)
        parse_ind_data(resp3, new_url)

# def start_thread(url):
#     resp = make_request(url)
#     response = scrapy.Selector(text=resp.content.decode('utf-8'))
#     try:
#         T_page = int(response.css('.m-page form a')[-2].css('::text').extract_first())
#     except:
#         T_page = 1
#     page = 1
#     while page <= T_page:
#         newUrl = url + '-' + str(page)
#         page = page + 1
#         resp2 = make_request(newUrl)
#         parse(resp2, newUrl)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('http://www.molbase.com/moldata/category-166')
    headers = dict([v for v in driver.requests if 'http://www.molbase.com/moldata/category-166' == v.url][0].headers)
    del headers['Accept-Encoding']
    driver.close()

    threads = []
    file_input = open('category_link.txt', 'r')
    input_list = file_input.read()
    for url in input_list.split('\n')[:5]:
        resp = make_request(url)
        response = scrapy.Selector(text=resp.content.decode('utf-8'))
        try:
            T_page = int(response.css('.m-page form a')[-2].css('::text').extract_first())
        except:
            T_page = 1
        page = 1
        while page <= T_page:
            newUrl = url + '-' + str(page)
            page = page + 1
            resp2 = make_request(newUrl)
            parse(resp2, newUrl)

    #     t = Thread(target=start_thread,args=(url,))
    #     t.start()
    #     threads.append(t)
    # for t in threads:
    #     t.join()


        # resp = make_request(url)
        # response = scrapy.Selector(text=resp.content.decode('utf-8'))
        # try:
        #     T_page = int(response.css('.m-page form a')[-2].css('::text').extract_first())
        # except:
        #     T_page = 1
        # page = 1
        # while page <= T_page:
        #     newUrl = url + '-' + str(page)
        #     page = page + 1
        #     resp2 = make_request(newUrl)
        #     parse(resp2, newUrl)

