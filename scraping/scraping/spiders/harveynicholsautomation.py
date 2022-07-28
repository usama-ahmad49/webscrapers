import csv
import datetime
import json
import re
import time

import csvdiff
import requests
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": 'CACHED_FRONT_FORM_KEY=IAj0lbdeJmlCjdV6; hn.geo.site-entry=1; hn.customer.channel=desktop; GlobalE_CT_Data=%7B%22CUID%22%3A%22795680064.856440148.502%22%2C%22CHKCUID%22%3Anull%7D; GlobalE_SupportThirdPartCookies=true; GlobalE_Full_Redirect=false; hn.nonEssentialCookiesRejected=0; hn.pecr.explicit=1; hn.pecr=1111/; _cs_c=1; _gcl_au=1.1.266149794.1631084841; tms_VisitorID=dms4o5svdp; hero-user-id=null; hn.product.imageView=item; REVLIFTER={"w":"c355b7e4-22f1-43b7-84cb-debc72b8cf89","u":"246bffa2-98fe-4426-8d8e-10f6270b716b","s":"7a04e67d-90f7-4dbc-bb9d-0ec768967204","se":1636269043}; token=0; CART_ITEMS_QUANTITY=%7B%22default%22%3A0%2C%22int%22%3A0%7D; CART_TOTAL=%7B%22default%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%2C%22int%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%7D; rskxRunCookie=0; rCookie=nx6cmszgz9a00fyz3n9umkumb4cpg; _ga_LEC37WCWGR=GS1.1.1634730719.32.0.1634730719.0; frontend=opd9qgpdascf00fmi4i02gafjs; cookies_populated=1; _cs_mk=0.9433546029411881_1635754592390; cs_hour_session=13; _gid=GA1.2.1501629965.1635754593; hn.geo.switcher=globale; _cs_cvars=%7B%2215%22%3A%5B%22h_deb_session%22%2C%2213%22%5D%7D; _ata_pow=1966; tms_wsip=1; bounceClientVisit4530v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0cAhgE4BuApgJ4B2AlgMZwD2YKZ7XALZEQAGhDUYIMSBT0A5jADaAXQC+QA; _sp_ses.30ed=*; GlobalE_Gem_Data=%7B%22CartID%22%3A%220%22%2C%22UserId%22%3A0%2C%22PreferedCulture%22%3A%22en_GB%22%2C%22StoreCode%22%3A%22default%22%7D; VIEWED_PRODUCT_IDS=4076962%2C4122006%2C4104338%2C4090440%2C4066382; _sp_id.30ed=04206fcb-6d7a-4730-a9da-3c7ce0affc99.1631084852.22.1635754683.1634727998.6628b2be-d08f-4bb8-86a5-dcde9e977dce; hn.customer.dept=womens; cto_bundle=a0XbZF9LT3NIcFlKdENJYTl5UUVWY1A1YlRjeWZyRzduUyUyRm52bWZDNWV0Y1doSkF4UkRDSWNCSmlBVlB1JTJCQlMwNmtqanlVJTJGVm1JaFZPVDJFWldrVndXUngxTThyZzVqJTJGYXdmVzlaZGtvUDZ2N0xwSXdWcllIejJCMWxGS1h6dldHVzdqSXEwU0FDNXlaOUwyNnI1UHdVQ29SdyUzRCUzRA; hn.globale.country=AE; hn.globale.currency=GBP; _mitata=M2MyZDFhNGUyMzY4ZWQ2ZWZmYmNjOTJhMDgwYTAwYThmNmRmZDAyYjM3NmIxZDljMzUzODQ1YTU2ZDU5MDI2ZQ==_/@#/1635755142_/@#/morx0kmi0yfsfpxs_/@#/000; _ga_XJ3X3ZTQGE=GS1.1.1635754614.1.1.1635755085.0; GlobalE_Data={%22countryISO%22:%22AE%22%2C%22currencyCode%22:%22GBP%22%2C%22cultureCode%22:%22en-GB%22}; hero-state-e50efedf-af83-4144-9e3c-1d35b94ca6cd={%22app%22:{%22launcherPush%22:{%22lastCloseTime%22:null%2C%22lastOpenTime%22:1635754987260}%2C%22status%22:{%22autoOpenAbility%22:true%2C%22isOpen%22:false%2C%22everOpened%22:false}}%2C%22channel%22:{%22lastSelectedId%22:null%2C%22listSize%22:0%2C%22listStatusIsInProgress%22:false}%2C%22customerService%22:{%22provider%22:null%2C%22conversationId%22:null%2C%22supportSessionId%22:null}%2C%22redirect%22:{%22reason%22:null}%2C%22_persist%22:{%22version%22:-1%2C%22rehydrated%22:true}%2C%22user%22:{}}; hero-session-e50efedf-af83-4144-9e3c-1d35b94ca6cd=author=client&expires=1667291087969&visitor=04f30a32-93ad-40d3-99cb-ad34423ec83c; _uetsid=064d9a903aec11ec83baf771be15419f; _uetvid=699faa00107311ec8d4351d0ffb40580; _ga_YFRVKPJD79=GS1.1.1635754593.1.1.1635755088.0; _dc_gtm_UA-1006476-1=1; _ga=GA1.2.160965070.1631022945; stc115044=env:1635754593%7C20211202081633%7C20211101085448%7C11%7C1045819:20221101082448|uid:1631084828662.609925542.7954836.115044.1311283153.:20221101082448|srchist:1045819%3A1635754593%3A20211202081633:20221101082448|tsa:1635754593802.625398983.6266098.31866706619881335.:20211101085448; _cs_id=502adf5e-2c90-a226-ab66-e2ed84c778bc.1631084827.26.1635755088.1635754593.1.1665248827015; _cs_s=11.0.0.1635756888838; lastRskxRun=1635755089147',
    "dnt": "1",
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": '?1',
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
headerswatch = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'CACHED_FRONT_FORM_KEY=IAj0lbdeJmlCjdV6; hn.geo.site-entry=1; hn.customer.channel=desktop; GlobalE_CT_Data=%7B%22CUID%22%3A%22795680064.856440148.502%22%2C%22CHKCUID%22%3Anull%7D; GlobalE_SupportThirdPartCookies=true; GlobalE_Full_Redirect=false; hn.nonEssentialCookiesRejected=0; hn.pecr.explicit=1; hn.pecr=1111/; _cs_c=1; _gcl_au=1.1.266149794.1631084841; tms_VisitorID=dms4o5svdp; hero-user-id=null; hn.product.imageView=item; REVLIFTER={"w":"c355b7e4-22f1-43b7-84cb-debc72b8cf89","u":"246bffa2-98fe-4426-8d8e-10f6270b716b","s":"7a04e67d-90f7-4dbc-bb9d-0ec768967204","se":1636269043}; token=0; CART_ITEMS_QUANTITY=%7B%22default%22%3A0%2C%22int%22%3A0%7D; CART_TOTAL=%7B%22default%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%2C%22int%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%7D; rskxRunCookie=0; rCookie=nx6cmszgz9a00fyz3n9umkumb4cpg; _ga_LEC37WCWGR=GS1.1.1634730719.32.0.1634730719.0; frontend=opd9qgpdascf00fmi4i02gafjs; _cs_mk=0.9433546029411881_1635754592390; cs_hour_session=13; _gid=GA1.2.1501629965.1635754593; hn.geo.switcher=globale; _cs_cvars=%7B%2215%22%3A%5B%22h_deb_session%22%2C%2213%22%5D%7D; _ata_pow=1966; tms_wsip=1; bounceClientVisit4530v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0cAhgE4BuApgJ4B2AlgMZwD2YKZ7XALZEQAGhDUYIMSBT0A5jADaAXQC+QA; _sp_ses.30ed=*; GlobalE_Gem_Data=%7B%22CartID%22%3A%220%22%2C%22UserId%22%3A0%2C%22PreferedCulture%22%3A%22en_GB%22%2C%22StoreCode%22%3A%22default%22%7D; VIEWED_PRODUCT_IDS=4076962%2C4122006%2C4104338%2C4090440%2C4066382; _sp_id.30ed=04206fcb-6d7a-4730-a9da-3c7ce0affc99.1631084852.22.1635754683.1634727998.6628b2be-d08f-4bb8-86a5-dcde9e977dce; hn.customer.dept=womens; hn.globale.country=AE; hn.globale.currency=GBP; _ga_XJ3X3ZTQGE=GS1.1.1635754614.1.1.1635755085.0; GlobalE_Data={%22countryISO%22:%22AE%22%2C%22currencyCode%22:%22GBP%22%2C%22cultureCode%22:%22en-GB%22}; lastRskxRun=1635755089147; _dc_gtm_UA-1006476-1=1; _mitata=ZTkyZTcxMDgwZjRiMmVlNzJkOWFlZGJmOGM5Njc1OWY0NGMzY2I2MzdmZjkyMjY3ZmM1MjU0MjE5NmRjYjM2ZQ==_/@#/1635756162_/@#/morx0kmi0yfsfpxs_/@#/000; cookies_populated=1; _uetsid=064d9a903aec11ec83baf771be15419f; _uetvid=699faa00107311ec8d4351d0ffb40580; stc115044=env:1635754593%7C20211202081633%7C20211101091145%7C13%7C1045819:20221101084145|uid:1631084828662.609925542.7954836.115044.1311283153.:20221101084145|srchist:1045819%3A1635754593%3A20211202081633:20221101084145|tsa:1635754593802.625398983.6266098.31866706619881335.:20211101091145; _cs_id=502adf5e-2c90-a226-ab66-e2ed84c778bc.1631084827.26.1635756105.1635754593.1.1665248827015; _cs_s=13.0.0.1635757905832; hero-session-e50efedf-af83-4144-9e3c-1d35b94ca6cd=author=client&expires=1667292106876&visitor=04f30a32-93ad-40d3-99cb-ad34423ec83c; _ga_YFRVKPJD79=GS1.1.1635754593.1.1.1635756107.0; _ga=GA1.1.160965070.1631022945; cto_bundle=6CHziV9LT3NIcFlKdENJYTl5UUVWY1A1YlRkUVFXcnQlMkIxVnVRS3VMNjBJQyUyQk9wOW9ZWlBDNkhUZVMzUHRVb2xBak4lMkJyWml6TGRGZmE0THJxek1iJTJGVUFTUVZBam5aVTBhMDNFSm04NzNoUmlhMjdMSlpiVlM1VGZwbk0lMkJ2Q000aU9iNjlkd01rNEVpVnV4VzdtbVVTdnJTeSUyRmclM0QlM0Q; hero-state-e50efedf-af83-4144-9e3c-1d35b94ca6cd={%22app%22:{%22launcherPush%22:{%22lastCloseTime%22:null%2C%22lastOpenTime%22:1635756114427}%2C%22status%22:{%22autoOpenAbility%22:true%2C%22isOpen%22:false%2C%22everOpened%22:false}}%2C%22channel%22:{%22lastSelectedId%22:null%2C%22listSize%22:0%2C%22listStatusIsInProgress%22:false}%2C%22customerService%22:{%22provider%22:null%2C%22conversationId%22:null%2C%22supportSessionId%22:null}%2C%22redirect%22:{%22reason%22:null}%2C%22_persist%22:{%22version%22:-1%2C%22rehydrated%22:true}}',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
# fileout = open('harveynichols.csv', 'w', newline='', encoding='utf-8')
# writer = csv.DictWriter(fileout, fieldnames=headers_csv)
# writer.writeheader()
# file_harveynichols = open('harveynichols_.txt', 'w')

'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
pricemagentoHNfile = open('harveynichols_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricemagentowriterHN = csv.DictWriter(pricemagentoHNfile, fieldnames=priceupdateheaders)
pricemagentowriterHN.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
priceodooHNfile = open('harveynichols_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
priceodoowriterHN = csv.DictWriter(priceodooHNfile, fieldnames=pricelistheaders)
priceodoowriterHN.writeheader()


def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


class harveynichols(scrapy.Spider):
    name = 'cettire'
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES': 30,
        'RETRY_HTTP_CODES': [301, 503],
    }

    def start_requests(self):
        '''women shoes'''
    #     url1 = 'https://www.harveynichols.com/int/womens/all-shoes/'
    #     while True:
    #         response = requests.get(url=url1, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice1 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice1 = 1
    #     # TotalPrice1 = 1
    #     for i in range(1, TotalPrice1 + 1):
    #         link1 = f'https://www.harveynichols.com/int/womens/all-shoes//page={i}/'
    #         yield scrapy.Request(url=link1, headers=header, meta={'gender': 'women', 'category': 'shoes'})
    #
    #     '''men shoes'''
    #     url2 = 'https://www.harveynichols.com/mens/all-shoes/'
    #     while True:
    #         response = requests.get(url=url2, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice2 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice2 = 1
    #
    #     for i2 in range(1, TotalPrice2 + 1):
    #         link = f'https://www.harveynichols.com/mens/all-shoes//page={i2}/'
    #         yield scrapy.Request(url=link, headers=header, meta={'gender': 'men', 'category': 'shoes'})
    #
    #     '''kids boys Shoes'''
    #     url3 = 'https://www.harveynichols.com/kidswear/boys/all-shoes/'
    #     while True:
    #         response = requests.get(url=url3, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice3 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice3 = 1
    #
    #     for i3 in range(1, TotalPrice3 + 1):
    #         link = f'https://www.harveynichols.com/kidswear/boys/all-shoes//page={i3}/'
    #         yield scrapy.Request(url=link, headers=header, meta={'gender': 'Kids-Boys', 'category': 'shoes'})
    #
    #     '''kids girl Shoes'''
    #     url4 = 'https://www.harveynichols.com/kidswear/girls/all-shoes/'
    #     while True:
    #         response = requests.get(url=url4, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice4 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice4 = 1
    #
    #     for i4 in range(1, TotalPrice4 + 1):
    #         link = f'https://www.harveynichols.com/kidswear/girls/all-shoes//page={i4}/'
    #         yield scrapy.Request(url=link, headers=header, meta={'gender': 'Kids-Girls', 'category': 'shoes'})
    #
    #     '''women bags'''
    #     url5 = 'https://www.harveynichols.com/womens/all-accessories/bags/'
    #     while True:
    #         response = requests.get(url=url5, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice5 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice5 = 1
    #
    #     for i5 in range(1, TotalPrice5 + 1):
    #         link = f'https://www.harveynichols.com/womens/all-accessories/bags//page={i5}/'
    #         yield scrapy.Request(url=link, headers=header, meta={'gender': 'Women', 'category': 'Bags'})
    #
    #     '''men bags'''
    #     url6 = 'https://www.harveynichols.com/mens/all-accessories/bags/'
    #     while True:
    #         response = requests.get(url=url6, headers=header)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice6 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice6 = 1
    #
    #     for i6 in range(1, TotalPrice6 + 1):
    #         link = f'https://www.harveynichols.com/mens/all-accessories/bags//page={i6}/'
    #         yield scrapy.Request(url=link, headers=header, meta={'gender': 'Men', 'category': 'Bags'})
    #
    #     '''women watches'''
    #     url7 = 'https://www.harveynichols.com/womens/all-accessories/watches/'
    #     while True:
    #         response = requests.get(url=url7, headers=headerswatch)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice7 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice7 = 1
    #
    #     for i7 in range(1, TotalPrice7 + 1):
    #         link = f'https://www.harveynichols.com/womens/all-accessories/watches//page={i7}/'
    #         yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Women', 'category': 'Watches'})
    #
    #     '''men watches'''
    #     url8 = 'https://www.harveynichols.com/mens/all-accessories/watches/'
    #     while True:
    #         response = requests.get(url=url8, headers=headerswatch)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice8 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice8 = 1
    #
    #     for i8 in range(1, TotalPrice8 + 1):
    #         link = f'https://www.harveynichols.com/mens/all-accessories/watches//page={i8}/'
    #         yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Men', 'category': 'Watches'})
    #
    #     '''men sunglasses'''
    #     url9 = 'https://www.harveynichols.com/mens/all-accessories/sunglasses/'
    #     while True:
    #         response = requests.get(url=url9, headers=headerswatch)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice9 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice9 = 1
    #
    #     for i9 in range(1, TotalPrice9 + 1):
    #         link = f'https://www.harveynichols.com/mens/all-accessories/sunglasses//page={i9}/'
    #         yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Men', 'category': 'Sunglasses'})
    #
    #     '''women sunglasses'''
    #     url10 = 'https://www.harveynichols.com/womens/all-accessories/sunglasses/'
    #     while True:
    #         response = requests.get(url=url10, headers=headerswatch)
    #         if response.status_code == 200:
    #             break
    #         time.sleep(5)
    #     resp = scrapy.Selector(text=response.content.decode('utf-8'))
    #     try:
    #         TotalPrice10 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
    #     except:
    #         TotalPrice10 = 1
    #
    #     for i10 in range(1, TotalPrice10 + 1):
    #         link = f'https://www.harveynichols.com/womens/all-accessories/sunglasses//page={i10}/'
    #         yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Women', 'category': 'Sunglasses'})
    #
    # def parse(self, response, **kwargs):
    #     for url in response.css('.items__list .product::attr(href)').extract():
    #         yield scrapy.Request(url='https://www.harveynichols.com/' + url, headers=header, callback=self.parse_data, meta={'gender': response.meta['gender'], 'category': response.meta['category']})
    #
    # def parse_data(self, response):
    #     try:
    #         jsonstr = [v for v in response.css('script::text').extract() if 'dataLayer.push' in v][0].split('dataLayer.push(')[-1].split(');')[0]
    #         dataB = json.loads(jsonstr)
    #         data = dataB['product']
    #         item = dict()
    #         item['serial_no'] = data['upc']
    #         item['ref'] = TS
    #         item['product_type'] = data['type']
    #         for clr in data['colour'].split():
    #             if check_color(clr):
    #                 item['color'] = clr
    #         if 'color' not in item.keys():
    #             item['color'] = data['colour']
    #         if 'h2d' in item['color']:
    #             item['color'] = item['color'].split('_')[0]
    #         item['product_type'] = response.url
    #         item['group_sku'] = data['dimension4'] + '-' + item['color'].title()
    #         item['style_id'] = data['dimension1']
    #         item['brand'] = data['brand']
    #         item['name_en'] = data['name']
    #         item['original_price'] = int(data['price'])
    #         item['strike_through_price'] = ''
    #         item['retail_price'] = int(data['price'])
    #         item['whole_sale_price'] = int(data['price'])
    #         item['description_en'] = data['description']
    #         item['gender'] = response.meta['gender']
    #         item['main_category'] = response.meta['gender']
    #         item['category'] = response.meta['category']
    #         item['sub_category'] = data['name'].split()[-1]
    #         item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
    #         item['origin'] = 'website'
    #         try:
    #             item['size_slug'] = [re.findall(r'(\w+?)(\d+)', data['availableSizes'][0])[0]][0][0]
    #         except:
    #             item['size_slug'] = ''
    #         item['description_plain_en'] = data['description']
    #         item['delivery_information'] = '15 to 20 days'
    #         item['main_pic'] = data['image_url'].split('?')[0]
    #         for i, res in enumerate(response.css('.p-images__preview-swatches img')):
    #             if i > 36:
    #                 break
    #             item[f'pic_{i + 1}'] = res.css('::attr(src)').extract_first().split('?')[0]
    #         index = 0
    #         if isinstance(data['availableSizes'], list):
    #             sizelists = data['availableSizes']
    #         else:
    #             sizelists = data['sizes']
    #         for sz in sizelists:
    #             if sz.__len__() >= 3:
    #                 item[f'variant_{index + 1}'] = ''.join(list(sz)[2:])
    #             elif sz.__len__() < 3:
    #                 item[f'variant_{index + 1}'] = sz
    #             if sz.__len__() >= 7:
    #                 item[f'variant_{index + 1}'] = sz
    #             if 'One Size' in sz:
    #                 item[f'variant_{index + 1}'] = 'OS'
    #             # try:
    #             #     item['variant_{}'.format(index + 1)] = [re.findall(r'(\w+?)(\d+\.+\d)', sz)[0]][0][-1]
    #             # except:
    #             #     try:
    #             #         item['variant_{}'.format(index + 1)] = [re.findall(r'(\w+?)(\d+)', sz)[0]][0][-1]
    #             #     except:
    #             #         item[f'variant_{index + 1}'] = sz
    #             item[f'variant_{index + 1}_price'] = int(data['price'])
    #
    #             for i in range(0, 3):
    #                 PUitem = dict()
    #                 PUitem['sku'] = item['group_sku'] + '-' + item['variant_{}'.format(index + 1)]
    #                 if i == 0:
    #                     PUitem['store_view_code'] = 'en'
    #                     PUitem['price'] = int((25 + (0.85 * item['variant_{}_price'.format(index + 1)])) * 6.2)
    #                     PUitem['status'] = 1
    #                     if item['variant_{}_price'.format(index + 1)] == 0:
    #                         PUitem['price'] = 0
    #                         PUitem['status'] = 2
    #
    #                 elif i == 1:
    #                     PUitem['store_view_code'] = 'sa_en'
    #                     PUitem['price'] = int(((((25 + (0.85 * item['variant_{}_price'.format(index + 1)])) * 6.2) * 10) / 100) + (25 + (0.85 * item['variant_{}_price'.format(index + 1)])) * 6.2)
    #                     PUitem['status'] = 1
    #                     if item['variant_{}_price'.format(index + 1)] == 0:
    #                         PUitem['price'] = 0
    #                         PUitem['status'] = 2
    #                 elif i == 2:
    #                     PUitem['store_view_code'] = 'us_en'
    #                     PUitem['price'] = int(item['variant_{}_price'.format(index + 1)])
    #                     PUitem['status'] = 1
    #                     if item['variant_{}_price'.format(index + 1)] == 0:
    #                         PUitem['price'] = 0
    #                         PUitem['status'] = 2
    #                 pricemagentowriterHN.writerow(PUitem)
    #                 pricemagentoHNfile.flush()
    #
    #             PLitem = dict()
    #             PLitem['GROUP SKU'] = item['group_sku']
    #             PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + item['variant_{}'.format(index + 1)]
    #             PLitem['RETAIL PRICE'] = int((25 + (0.85 * item['variant_{}_price'.format(index + 1)])) * 6.2)
    #             if item['variant_{}_price'.format(index + 1)] == 0:
    #                 PLitem['RETAIL PRICE'] = 0
    #             PLitem['WEBSITES'] = 'United Arab Emirates'
    #             priceodoowriterHN.writerow(PLitem)
    #             priceodooHNfile.flush()
    #
    #             index += 1
    #     except:
    #         pass

    def close(self, reason):
        pricemagentoHNfile.close()
        priceodooHNfile.close()

        '''delta file for magento'''
        patch = csvdiff.diff_files('harveynichols_pricelist_magento_original.csv', 'harveynichols_pricelist_magento_temp.csv',
                                   ['sku', 'store_view_code'])
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('harveynichols_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('harveynichols_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)

        removed = []
        for item in patch['removed']:
            item__ = dict()
            item__['sku'] = item['sku']
            item__['store_view_code'] = item['store_view_code']
            item__['status'] = '2'
            item__['price'] = 0
            deltapricewriter.writerow(item__)
            deltapriceupdate.flush()
            removed.append(item__)

        for item in patch['added']:
            deltapricewriter.writerow(item)
            deltapriceupdate.flush()
            originalpriceupdatewriter.writerow(item)
            originalpriceupdate.flush()

        changed = []
        for item in patch['changed']:
            item_ = dict()
            item_['sku'] = item['key'][0]
            item_['store_view_code'] = item['key'][1]
            try:
                if item['fields']['price']['to'] != '0':
                    item_['status'] = '1'
                else:
                    item_['status'] = '2'
                item_['price'] = int(float(item['fields']['price']['to']))
            except:
                item_['status'] = item['fields']['status']['to']
                if item_['status'] == '2':
                    item_['price'] = '0'
            deltapricewriter.writerow(item_)
            deltapriceupdate.flush()
            changed.append(item_)
        original_list = list(csv.DictReader(open('harveynichols_pricelist_magento_original.csv')))
        originalpriceupdate = open('harveynichols_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = int(float(c_item['price']))
                    o_item['status'] = c_item['status']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file = open('harveynichols_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('harveynichols_pricelist_magento_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                skus_list_temp.append(row['sku'])

            magento_temp.close()

        for line in text_file.readlines():

            if line.strip() not in skus_list_temp:
                not_match_skus.append(line.strip())

        text_file.close()

        original_list = list(csv.DictReader(open('harveynichols_pricelist_magento_original.csv')))
        originalpriceupdate = open('harveynichols_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=['sku', 'price', 'status', 'store_view_code'])
        originalpriceupdatewriter.writeheader()

        for row in original_list:
            if row['sku'] in not_match_skus:
                row['price'] = 0
                row['status'] = 2
            originalpriceupdatewriter.writerow(row)
            originalpriceupdate.flush()

        ####        odoo code         ####

        patch_2 = csvdiff.diff_files('harveynichols_pricelist_odoo_original.csv', 'harveynichols_pricelist_odoo_temp.csv',
                                     ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        '''delta file for pricelist'''
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('harveynichols_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('harveynichols_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
        originalpricelistwriter = csv.DictWriter(originalpricelist, fieldnames=deltapricelistheaders)

        removed = []
        for item in patch_2['removed']:
            item__ = dict()
            item__['GROUP SKU'] = item['GROUP SKU']
            item__['PRODUCT SKU'] = item['PRODUCT SKU']
            item__['WEBSITES'] = item['WEBSITES']
            item__['RETAIL PRICE'] = 0
            deltapricelistwriter.writerow(item__)
            deltapricelistfile.flush()
            removed.append(item__)

        for item in patch_2['added']:
            deltapricelistwriter.writerow(item)
            deltapricelistfile.flush()
            originalpricelistwriter.writerow(item)
            originalpricelist.flush()

        changed = []
        for item in patch_2['changed']:
            item_ = dict()
            item_['GROUP SKU'] = item['key'][0]
            item_['PRODUCT SKU'] = item['key'][1]
            item_['WEBSITES'] = item['key'][2]
            item_['RETAIL PRICE'] = int(float(item['fields']['RETAIL PRICE']['to']))
            deltapricelistwriter.writerow(item_)
            deltapricelistfile.flush()
            changed.append(item_)

        original_list = list(csv.DictReader(open('harveynichols_pricelist_odoo_original.csv')))
        originalpriceupdate = open('harveynichols_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()

        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = int(float(c_item['RETAIL PRICE']))
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file_sku_still_available2 = open('harveynichols_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('harveynichols_pricelist_odoo_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                skus_list_temp.append(row['PRODUCT SKU'])

            magento_temp.close()

        for line in text_file_sku_still_available2.readlines():

            if line.strip() not in skus_list_temp:
                not_match_skus.append(line.strip())

        text_file_sku_still_available2.close()

        original_list = list(csv.DictReader(open('harveynichols_pricelist_odoo_original.csv')))
        originalpriceupdate = open('harveynichols_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES'])
        originalpriceupdatewriter.writeheader()

        for row in original_list:
            if row['PRODUCT SKU'] in not_match_skus:
                row['RETAIL PRICE'] = 0
            originalpriceupdatewriter.writerow(row)
            originalpriceupdate.flush()

        text_file_sku_update = open('harveynichols_skus.txt', 'a')
        for item in patch_2['added']:
            text_file_sku_update.write('\n' + item['PRODUCT SKU'])
            text_file_sku_update.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(harveynichols)
process.start()
