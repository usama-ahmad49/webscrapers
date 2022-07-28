import json
import csv
from selenium.webdriver.firefox.options import Options as ff_options
import scrapy
from scrapy.crawler import CrawlerProcess

EINinputlist = []
data_list = []
fileinput = open('open990org.csv', 'r', encoding='utf-8')
inputstrs = fileinput.read().split('\n')[1:]
for inputstr in inputstrs:
    EINinputlist.append(inputstr.split(',')[0])
for l in inputstrs[1:-1]:
    l = l.split(',')
    item = dict()
    item['EIN'] = '0' + l[0]
    item['NAME'] = l[1]
    item['ADDRESS LINE 1'] = l[2]
    item['ADDRESS LINE 2'] = l[3]
    item['CITY'] = l[4]
    item['STATE'] = l[5]
    item['POSTAL CODE'] = l[6]
    item['COUNTRY'] = l[7]
    item['ORG TYPE'] = l[8]
    item['NTEE CODE 1'] = l[9]
    item['NTEE CLASSIFICATION 1'] = l[10]
    item['NTEE CODE 2'] = l[11]
    item['NTEE CLASSIFICATION 2'] = l[12]
    item['NTEE CODE 3'] = l[13]
    item['NTEE CLASSIFICATION 3'] = l[14]
    item['MISSION'] = l[15]
    item['ALAIS'] = l[16]
    item['WEBSITE'] = l[17]
    item['FACEBOOK'] = l[18]
    item['TWITTER'] = l[19]
    item['INSTAGRAM'] = l[20]
    item['NTEE TYPE'] = l[21]
    item['WEBSITE URL'] = l[22]
    item['DESCRIPTION'] = l[23]
    data_list.append(item)

headers = ['EIN', 'NAME', 'ADDRESS LINE 1', 'ADDRESS LINE 2', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY', 'ORG TYPE', 'NTEE CODE 1', 'NTEE CLASSIFICATION 1', 'NTEE CODE 2', 'NTEE CLASSIFICATION 2', 'NTEE CODE 3', 'NTEE CLASSIFICATION 3', 'MISSION', 'ALAIS', 'WEBSITE', 'FACEBOOK', 'TWITTER', 'INSTAGRAM', 'NTEE TYPE', 'WEBSITE URL', 'DESCRIPTION', ]
fileout = open('guidstarspider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '__cfduid=d11e7607fe86639c49ef800d7349298051607923892; _ga=GA1.2.971163972.1607923950; _gid=GA1.2.777805520.1607923950; _hjTLDTest=1; _hjid=b89f5d8e-2d18-4494-93cb-4160e68d3e4a; cf_chl_1=a8b6c74b507811c; cf_chl_prog=a17; cf_clearance=a7288831fc9ac39148f4be9c4581eb8cbbbeacd3-1607928951-0-250',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

formdata = {
    'r': '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',
    'cf_captcha_kind': 'h',
    'vc': '598f08137ec1a0f7afe5a5cf9f87d6ad',
    'captcha_vc': 'b8546954cb048f4c7ec04362c076511c',
    'captcha_answer': 'sgsDghirkrUQ-11-60160e451814dcc2',
    'cf_ch_verify': 'plat',
    'h-captcha-response': 'captchka',
}


class open990org(scrapy.Spider):
    name = 'open990org'

    def start_requests(self):
        options = ff_options()
        options.add_argument('--headless')
        # driver=webdriver.Chrome()
        for ein in EINinputlist:
            if len(ein) > 7:
                ein = '0' + ein
                url = f'https://www.open990.org/api/org/skeleton/{ein}/'
                # driver.get(url=url)
                # driver.text
                # scraper = cfscrape.create_scraper()
                # responce=scraper.get(url=url).content
                yield scrapy.Request(url=url, body=json.dumps(formdata), headers=headers)

    def parse(self, response, **kwargs):
        pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(open990org)
process.start()
