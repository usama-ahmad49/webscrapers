import csv
import datetime
import json
import re
import time

import requests
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')

headers_csv = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'style_id', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "original_price", 'strike_through_price', 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
               'description_plain_en', 'delivery_information', 'main_pic',

               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9", "pic_10", "pic_11", "pic_12", "pic_13", "pic_14",
               "pic_15", "pic_16", "pic_17", "pic_18", "pic_19", "pic_20", "pic_21", "pic_22", "pic_23", "pic_24", "pic_25", "pic_26", "pic_27",
               "pic_28", "pic_29", "pic_30", "pic_31", "pic_32", "pic_33", "pic_34", "pic_35", "pic_36",

               "variant_1", "variant_1_price", "variant_2", "variant_2_price",
               "variant_3", "variant_3_price", "variant_4", "variant_4_price", "variant_5", "variant_5_price",
               "variant_6", "variant_6_price", "variant_7", "variant_7_price", "variant_8", "variant_8_price",
               "variant_9", "variant_9_price", "variant_10", "variant_10_price", "variant_11", "variant_11_price",
               "variant_12", "variant_12_price", "variant_13", "variant_13_price", "variant_14", "variant_14_price",
               "variant_15", "variant_15_price", "variant_16", "variant_16_price", "variant_17", "variant_17_price",
               "variant_18", "variant_18_price", "variant_19", "variant_19_price", "variant_20", "variant_20_price",
               "variant_21", "variant_21_price", "variant_22", "variant_22_price", "variant_23", "variant_23_price",
               "variant_24", "variant_24_price", "variant_25", "variant_25_price", "variant_26", "variant_26_price",
               "variant_27", "variant_27_price", "variant_28", "variant_28_price", "variant_29", "variant_29_price",
               "variant_30", "variant_30_price", "variant_31", "variant_31_price", "variant_32", "variant_32_price",
               "variant_33", "variant_33_price", "variant_34", "variant_34_price", "variant_35", "variant_35_price",
               "variant_36", "variant_36_price", "variant_37", "variant_37_price", "variant_38", "variant_38_price",
               "variant_39", "variant_39_price", "variant_40", "variant_40_price", "variant_41", "variant_41_price",
               "variant_42", "variant_42_price", "variant_43", "variant_43_price", "variant_44", "variant_44_price",
               "variant_45", "variant_45_price", "variant_46", "variant_46_price", "variant_47", "variant_47_price",
               "variant_48", "variant_48_price", "variant_49", "variant_49_price", "variant_50", "variant_50_price",
               "variant_51", "variant_51_price", "variant_52", "variant_52_price", "variant_53", "variant_53_price",
               "variant_54", "variant_54_price", "variant_55", "variant_55_price", "variant_56", "variant_56_price",
               "variant_57", "variant_57_price", "variant_58", "variant_58_price", "variant_59", "variant_59_price",
               "variant_60", "variant_60_price", "variant_61", "variant_61_price", "variant_62", "variant_62_price",
               "variant_63", "variant_63_price", "variant_64", "variant_64_price", "variant_65", "variant_65_price",
               "variant_66", "variant_66_price", "variant_67", "variant_67_price", "variant_68", "variant_68_price",
               "variant_69", "variant_69_price", "variant_70", "variant_70_price", "variant_71", "variant_71_price",
               "variant_72", "variant_72_price", "variant_73", "variant_73_price", "variant_74", "variant_74_price",
               "variant_75", "variant_75_price", "variant_76", "variant_76_price", "variant_77", "variant_77_price",
               "variant_78", "variant_78_price", "variant_79", "variant_79_price", "variant_80", "variant_80_price",
               "variant_81", "variant_81_price", "variant_82", "variant_82_price", "variant_83", "variant_83_price",
               "variant_84", "variant_84_price", "variant_85", "variant_85_price", "variant_86", "variant_86_price",
               "variant_87", "variant_87_price", "variant_88", "variant_88_price", "variant_89", "variant_89_price",
               "variant_90", "variant_90_price", "variant_91", "variant_91_price", "variant_92", "variant_92_price",
               "variant_93", "variant_93_price", "variant_94", "variant_94_price", "variant_95", "variant_95_price",
               "variant_96", "variant_96_price", "variant_97", "variant_97_price", "variant_98", "variant_98_price",
               "variant_99", "variant_99_price", "variant_100", "variant_100_price"
               ]

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": 'cs_hour_session=13; CACHED_FRONT_FORM_KEY=IAj0lbdeJmlCjdV6; hn.geo.site-entry=1; hn.customer.channel=desktop; hn.geo.switcher=globale; hn.globale.country=PK; _ata_pow=da3; _gid=GA1.2.1950517076.1631022945; token=0; GlobalE_CT_Data=%7B%22CUID%22%3A%22795680064.856440148.502%22%2C%22CHKCUID%22%3Anull%7D; GlobalE_SupportThirdPartCookies=true; GlobalE_Full_Redirect=false; GlobalE_Gem_Data=%7B%22CartID%22%3A%220%22%2C%22UserId%22%3A0%2C%22PreferedCulture%22%3A%22en_GB%22%2C%22StoreCode%22%3A%22int%22%7D; CART_ITEMS_QUANTITY=%7B%22default%22%3A0%2C%22int%22%3A0%7D; CART_TOTAL=%7B%22default%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%2C%22int%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%7D; frontend=kmq497ut6b6g062259hokh7nu0; hn.pecr.explicit=1; hn.nonEssentialCookiesRejected=0; hn.pecr=1111/; _cs_c=1; _gcl_au=1.1.266149794.1631084841; tms_VisitorID=dms4o5svdp; REVLIFTER={"w":"c355b7e4-22f1-43b7-84cb-debc72b8cf89","u":"246bffa2-98fe-4426-8d8e-10f6270b716b","s":"3b3fc15e-0016-40e0-be41-987f1a34b6d0","se":1633676842}; hero-user-id=null; _sp_ses.30ed=*; hn.globale.currency=USD; hn.customer.dept=womens; _cs_cvars=%7B%2215%22%3A%5B%22h_deb_session%22%2C%2213%22%5D%7D; VIEWED_PRODUCT_IDS=4082892; _sp_id.30ed=04206fcb-6d7a-4730-a9da-3c7ce0affc99.1631084852.2.1631088262.1631084995.5c79ec2c-600b-4026-a31c-e7cd5dbb5f90; hn.product.imageView=item; tms_wsip=1; cookies_populated=1; _mitata=OTg1ZjkyNmIwMGM5MDQ2NzRkNGM4ZjEyNjY4MjQ2NDhiOTM5ZWE3MzQ3NTFhNzFhM2IyZDM2ZjgxMDEzODQxZg==_/@#/1631089146_/@#/mxbymk1uvetgrjab_/@#/000; _cs_mk=0.8906967112536794_1631089102469; bounceClientVisit4530v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0cAhgE4BuApgJ4B2AlgMZwD2YKZ7XALZFWzBEWJD6zdAUpgwAWhTd6swgQiUA5vUwARAGxEQAGhDUYIMyBT1tMANoBdAL5A; _ga=GA1.2.160965070.1631022945; _ga_LEC37WCWGR=GS1.1.1631087180.4.1.1631089112.0; GlobalE_Data=%7B%22countryISO%22%3A%22PK%22%2C%22currencyCode%22%3A%22USD%22%2C%22cultureCode%22%3A%22en-GB%22%7D; _uetsid=699f6830107311ecaf3df79ba54b3af1; _uetvid=699faa00107311ec8d4351d0ffb40580; stc115044=env:1631087182%7C20211009074622%7C20210908084833%7C14%7C1045819:20220908081833|uid:1631084828662.609925542.7954836.115044.1311283153.:20220908081833|srchist:1045819%3A1631087182%3A20211009074622:20220908081833|tsa:1631087182540.1151862816.1359615.7493765544727435.:20210908084833; _cs_id=502adf5e-2c90-a226-ab66-e2ed84c778bc.1631084827.2.1631089113.1631087170.1.1665248827015; _cs_s=20.0.0.1631090913869; hero-session-e50efedf-af83-4144-9e3c-1d35b94ca6cd=author=client&expires=1662625114787&visitor=04f30a32-93ad-40d3-99cb-ad34423ec83c; cto_bundle=M4b0Cl9LT3NIcFlKdENJYTl5UUVWY1A1YlRhZ0lLZHdhUmY5WG5JNndCYW9YRlYyZGhZRlNhZXBKOCUyQmRUYm9Ub3VZSWQwUzlhMEtyNkdSbWslMkYlMkY0YVNSYzhEUnBaJTJCbUVrYnQ4OHBYUTFkTHplS1ZLY3VhNXY3VWtzZzRGOVZLUjRIVlNUUGF3ZGh5RjNoQzZaWVlhWWJZSWNTQSUzRCUzRA; hero-state-e50efedf-af83-4144-9e3c-1d35b94ca6cd={%22app%22:{%22launcherPush%22:{%22lastCloseTime%22:1631088489331%2C%22lastOpenTime%22:1631088219765}%2C%22status%22:{%22autoOpenAbility%22:true%2C%22isOpen%22:false%2C%22everOpened%22:false}}%2C%22channel%22:{%22lastSelectedId%22:null%2C%22listSize%22:0%2C%22listStatusIsInProgress%22:false}%2C%22redirect%22:{%22reason%22:null}%2C%22_persist%22:{%22version%22:-1%2C%22rehydrated%22:true}}',
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
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": 'cs_hour_session=19; CACHED_FRONT_FORM_KEY=IAj0lbdeJmlCjdV6; hn.geo.site-entry=1; hn.customer.channel=desktop; hn.geo.switcher=globale; _gid=GA1.2.1950517076.1631022945; token=0; GlobalE_CT_Data=%7B%22CUID%22%3A%22795680064.856440148.502%22%2C%22CHKCUID%22%3Anull%7D; GlobalE_SupportThirdPartCookies=true; GlobalE_Full_Redirect=false; CART_ITEMS_QUANTITY=%7B%22default%22%3A0%2C%22int%22%3A0%7D; CART_TOTAL=%7B%22default%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%2C%22int%22%3A%7B%22subtotal%22%3A0%2C%22grand_total%22%3Anull%2C%22giftwrapping%22%3A0%2C%22subtotal_formatted%22%3A%22%5Cu00a30.00%22%7D%7D; hn.nonEssentialCookiesRejected=0; hn.pecr.explicit=1; hn.pecr=1111/; _cs_c=1; _gcl_au=1.1.266149794.1631084841; tms_VisitorID=dms4o5svdp; REVLIFTER={"w":"c355b7e4-22f1-43b7-84cb-debc72b8cf89","u":"246bffa2-98fe-4426-8d8e-10f6270b716b","s":"3b3fc15e-0016-40e0-be41-987f1a34b6d0","se":1633676842}; hero-user-id=null; hn.product.imageView=item; hn.globale.currency=GBP; hn.globale.country=GB; GlobalE_Data={%22countryISO%22:%22GB%22%2C%22currencyCode%22:%22GBP%22%2C%22cultureCode%22:%22en-GB%22}; GlobalE_Gem_Data=%7B%22CartID%22%3A%220%22%2C%22UserId%22%3A0%2C%22PreferedCulture%22%3A%22en_GB%22%2C%22StoreCode%22%3A%22default%22%7D; VIEWED_PRODUCT_IDS=4122810%2C4082892; _ga=GA1.2.160965070.1631022945; _sp_id.30ed=04206fcb-6d7a-4730-a9da-3c7ce0affc99.1631084852.6.1631106389.1631098767.bcd5a1ab-e15e-4d18-b70f-71c7473a3e6d; _ata_pow=858; _ga_LEC37WCWGR=GS1.1.1631109383.9.1.1631109384.0; _mitata=YTVhODZjYmNjOTJkNzgzMmFlZWRmYjNjMzljOTcwNjA3NDE5YzU5ODQ1NzJmYTczZmFjZWYyNTEwZTJlMThmMg==_/@#/1631110865_/@#/mxbymk1uvetgrjab_/@#/000; frontend=nqitj0qi5k4d3u93gn5kb96o40; cookies_populated=1; hn.customer.dept=womens; _cs_mk=0.38156547901549853_1631110808852; stc115044=env:1631110809%7C20211009142009%7C20210908145009%7C1%7C1045819:20220908142009|uid:1631084828662.609925542.7954836.115044.1311283153.:20220908142009|srchist:1045819%3A1631110809%3A20211009142009:20220908142009|tsa:1631110809207.1351961717.0845108.7931694897351951.:20210908145009; _cs_cvars=%7B%2215%22%3A%5B%22h_deb_session%22%2C%2219%22%5D%7D; _cs_id=502adf5e-2c90-a226-ab66-e2ed84c778bc.1631084827.7.1631110809.1631110809.1.1665248827015; _cs_s=1.0.0.1631112609283; _uetsid=699f6830107311ecaf3df79ba54b3af1; _uetvid=699faa00107311ec8d4351d0ffb40580; _dc_gtm_UA-1006476-1=1; tms_wsip=1; hero-session-e50efedf-af83-4144-9e3c-1d35b94ca6cd=author=client&expires=1662646810534&visitor=04f30a32-93ad-40d3-99cb-ad34423ec83c; _gat_UA-1006476-1=1; cto_bundle=4cGCQF9LT3NIcFlKdENJYTl5UUVWY1A1YlRSU2hnNVhsZTJ5SkJidVVBSGolMkZsUE9UQyUyRkxXNlZ5YmV0SzNQdlhEWlQlMkZKc2hPWUZDNWYlMkZvQ0VJWmRKJTJCSlJYejFJTHY1b0pGdk1laGtVZkdQSnlPU0VLZjJBMWhkekM2ckpLWkpZeU5lWUN0RnAzREF0NmwlMkYwJTJCTzBUa0Fta0ZGQSUzRCUzRA; hero-state-e50efedf-af83-4144-9e3c-1d35b94ca6cd={%22app%22:{%22launcherPush%22:{%22lastCloseTime%22:1631088489331%2C%22lastOpenTime%22:1631088219765}%2C%22status%22:{%22autoOpenAbility%22:true%2C%22isOpen%22:false%2C%22everOpened%22:false}}%2C%22channel%22:{%22lastSelectedId%22:null%2C%22listSize%22:0%2C%22listStatusIsInProgress%22:false}%2C%22redirect%22:{%22reason%22:null}%2C%22_persist%22:{%22version%22:-1%2C%22rehydrated%22:true}}',
    "dnt": '1',
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": '1',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
fileout = open('harveynichols.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()
file_harveynichols = open('harveynichols_.txt', 'w')


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
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [301, 503],
    }

    def start_requests(self):
        '''women shoes'''
        url1 = 'https://www.harveynichols.com/int/womens/all-shoes/'
        while True:
            response = requests.get(url=url1, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice1 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice1 = 1

        for i in range(1, TotalPrice1 + 1):
            link1 = f'https://www.harveynichols.com/int/womens/all-shoes//page={i}/'
            yield scrapy.Request(url=link1, headers=header, meta={'gender': 'women', 'category': 'shoes'})

        '''men shoes'''
        url2 = 'https://www.harveynichols.com/mens/all-shoes/'
        while True:
            response = requests.get(url=url2, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice2 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice2 = 1

        for i2 in range(1, TotalPrice2 + 1):
            link = f'https://www.harveynichols.com/mens/all-shoes//page={i2}/'
            yield scrapy.Request(url=link, headers=header, meta={'gender': 'men', 'category': 'shoes'})

        '''kids boys Shoes'''
        url3 = 'https://www.harveynichols.com/kidswear/boys/all-shoes/'
        while True:
            response = requests.get(url=url3, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice3 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice3 = 1

        for i3 in range(1, TotalPrice3 + 1):
            link = f'https://www.harveynichols.com/kidswear/boys/all-shoes//page={i3}/'
            yield scrapy.Request(url=link, headers=header, meta={'gender': 'Kids-Boys', 'category': 'shoes'})

        '''kids girl Shoes'''
        url4 = 'https://www.harveynichols.com/kidswear/girls/all-shoes/'
        while True:
            response = requests.get(url=url4, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice4 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice4 = 1

        for i4 in range(1, TotalPrice4 + 1):
            link = f'https://www.harveynichols.com/kidswear/girls/all-shoes//page={i4}/'
            yield scrapy.Request(url=link, headers=header, meta={'gender': 'Kids-Girls', 'category': 'shoes'})

        '''women bags'''
        url5 = 'https://www.harveynichols.com/womens/all-accessories/bags/'
        while True:
            response = requests.get(url=url5, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice5 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice5 = 1

        for i5 in range(1, TotalPrice5 + 1):
            link = f'https://www.harveynichols.com/womens/all-accessories/bags//page={i5}/'
            yield scrapy.Request(url=link, headers=header, meta={'gender': 'Women', 'category': 'Bags'})

        '''men bags'''
        url6 = 'https://www.harveynichols.com/mens/all-accessories/bags/'
        while True:
            response = requests.get(url=url6, headers=header)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice6 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice6 = 1

        for i6 in range(1, TotalPrice6 + 1):
            link = f'https://www.harveynichols.com/mens/all-accessories/bags//page={i6}/'
            yield scrapy.Request(url=link, headers=header, meta={'gender': 'Men', 'category': 'Bags'})

        '''women watches'''
        url7 = 'https://www.harveynichols.com/womens/all-accessories/watches/'
        while True:
            response = requests.get(url=url7, headers=headerswatch)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice7 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice7 = 1

        for i7 in range(1, TotalPrice7 + 1):
            link = f'https://www.harveynichols.com/womens/all-accessories/watches//page={i7}/'
            yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Women', 'category': 'Watches'})

        '''men watches'''
        url8 = 'https://www.harveynichols.com/mens/all-accessories/watches/'
        while True:
            response = requests.get(url=url8, headers=headerswatch)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice8 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice8 = 1

        for i8 in range(1, TotalPrice8 + 1):
            link = f'https://www.harveynichols.com/mens/all-accessories/watches//page={i8}/'
            yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Men', 'category': 'Watches'})

        '''men sunglasses'''
        url9 = 'https://www.harveynichols.com/mens/all-accessories/sunglasses/'
        while True:
            response = requests.get(url=url9, headers=headerswatch)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice9 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice9 = 1

        for i9 in range(1, TotalPrice9 + 1):
            link = f'https://www.harveynichols.com/mens/all-accessories/sunglasses//page={i9}/'
            yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Men', 'category': 'Sunglasses'})

        '''women sunglasses'''
        url10 = 'https://www.harveynichols.com/womens/all-accessories/sunglasses/'
        while True:
            response = requests.get(url=url10, headers=headerswatch)
            if response.status_code == 200:
                break
            time.sleep(5)
        resp = scrapy.Selector(text=response.content.decode('utf-8'))
        try:
            TotalPrice10 = int(resp.css('ul.pagination__links li a span::text').extract()[-1])
        except:
            TotalPrice10 = 1

        for i10 in range(1, TotalPrice10 + 1):
            link = f'https://www.harveynichols.com/womens/all-accessories/sunglasses//page={i10}/'
            yield scrapy.Request(url=link, headers=headerswatch, meta={'gender': 'Women', 'category': 'Sunglasses'})

    def parse(self, response, **kwargs):
        for url in response.css('.items__list .product::attr(href)').extract():
            yield scrapy.Request(url='https://www.harveynichols.com/' + url, callback=self.parse_data, meta={'gender': response.meta['gender'], 'category': response.meta['category']})
            # yield scrapy.Request(url='https://www.harveynichols.com/int/brand/moncler/449448-ariel-white-leather-sneakers/p4077745/' ,callback=self.parse_data, meta={'gender':response.meta['gender'], 'category':response.meta['category']})

    def parse_data(self, response):
        try:
            jsonstr = [v for v in response.css('script::text').extract() if 'dataLayer.push' in v][0].split('dataLayer.push(')[-1].split(');')[0]
            dataB = json.loads(jsonstr)
            data = dataB['product']
            item = dict()
            item['serial_no'] = data['upc']
            item['ref'] = TS
            item['product_type'] = data['type']
            for clr in data['colour'].split():
                if check_color(clr):
                    item['color'] = clr
            if 'color' not in item.keys():
                item['color'] = data['colour'].split()[0]
            item['group_sku'] = response.url
            item['product_type'] = data['dimension4'] + '-' + item['color']
            # item['group_sku'] = data['dimension4'] + '-' + item['color']
            item['style_id'] = data['dimension1']
            item['brand'] = data['brand']
            item['name_en'] = data['name']
            item['original_price'] = str(data['price']) + ' ' + dataB['ecommerce']['currencyCode']
            item['strike_through_price'] = ''
            item['retail_price'] = str(data['price']) + ' ' + dataB['ecommerce']['currencyCode']
            item['whole_sale_price'] = str(data['price']) + ' ' + dataB['ecommerce']['currencyCode']
            item['description_en'] = data['description']
            item['gender'] = response.meta['gender']
            item['main_category'] = response.meta['gender']
            item['category'] = response.meta['category']
            item['sub_category'] = data['name'].split()[-1]
            item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
            item['origin'] = 'website'
            try:
                item['size_slug'] = [re.findall(r'(\w+?)(\d+)', data['availableSizes'][0])[0]][0][0]
            except:
                item['size_slug'] = ''
            item['description_plain_en'] = data['description']
            item['delivery_information'] = '15 to 20 days'
            item['main_pic'] = data['image_url'].split('?')[0]
            for i, res in enumerate(response.css('.p-images__preview-swatches img')):
                if i > 36:
                    break
                item[f'pic_{i + 1}'] = res.css('::attr(src)').extract_first().split('?')[0]
            index = 0
            for sz in data['availableSizes']:
                if sz.__len__()>=3:
                    item[f'variant_{index + 1}'] = ''.join(list(sz)[2:])
                elif sz.__len__()<3:
                    item[f'variant_{index + 1}'] = sz
                if sz.__len__()>=7:
                    item[f'variant_{index + 1}'] = sz
                # if 'One Size' in sz:
                #     item[f'variant_{index + 1}'] = sz
                # try:
                #     item['variant_{}'.format(index + 1)] = [re.findall(r'(\w+?)(\d+\.+\d)', sz)[0]][0][-1]
                # except:
                #     try:
                #         item['variant_{}'.format(index + 1)] = [re.findall(r'(\w+?)(\d+)', sz)[0]][0][-1]
                #     except:
                #         item[f'variant_{index + 1}'] = sz
                item[f'variant_{index + 1}_price'] = str(data['price']) + ' ' + dataB['ecommerce']['currencyCode']
                index += 1
            writer.writerow(item)
            fileout.flush()
        except:
            file_harveynichols.write(response.url + '\n')
            file_harveynichols.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(harveynichols)
process.start()
