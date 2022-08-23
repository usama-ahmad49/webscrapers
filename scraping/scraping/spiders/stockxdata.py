import json
import os

import boto3
import requests
import scrapy
import wget
from botocore.exceptions import NoCredentialsError
from scrapy.crawler import CrawlerProcess
from word2number import w2n

cwd = os.getcwd()

headers = {
    'authority': 'stockx.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'app-platform': 'Iron',
    'app-version': '2022.07.31.05',
    'dnt': '1',
    'referer': 'https://stockx.com/adidas',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'X-Crawlera-Max-Retries': '1',
    'X-Crawlera-Profile': 'mobile',
    'X-Crawlera-Cookies': 'discard',
    'X-Crawlera-Region': 'ca'

}

cookies = {
    'stockx_market_country': 'PK',
    '_ga': 'GA1.2.788108403.1627381998',
    'pxcts': '0e9c4630-eec6-11eb-8f35-456c805b484e',
    '_scid': 'd66f0315-e66c-43f7-9088-cb913be1d684',
    'product_page_affirm_callout_enabled_web': 'false',
    'below_retail_type': '',
    'riskified_recover_updated_verbiage': 'true',
    'home_vertical_rows_web': 'true',
    '_px_f394gi7Fvmc43dfg_user_id': 'MTA0OTU5ZjEtZWVjNi0xMWViLTkzMWQtNzU0NDc2NWQ2YjUy',
    'QuantumMetricUserID': 'd09c7fd3ca35f4883252442e93c26ffb',
    'rskxRunCookie': '0',
    'rCookie': 'o5z2ngw5qrkce8yubt0e7tkrlx854q',
    'IR_gbd': 'stockx.com',
    '_rdt_uuid': '1627382004357.08170ccd-84e5-4727-b809-30b9e8d7868b',
    '__ssid': '3ff3af1fd98b9b60409658d135799ec',
    '__pxvid': '87150fcf-0428-11ec-a4f3-0242ac110002',
    '_ts_yjad': '1629827453266',
    'stockx_preferred_market_activity': 'sales',
    'stockx_dismiss_modal': 'true',
    'stockx_dismiss_modal_set': '2021-09-16T06%3A39%3A57.270Z',
    'stockx_dismiss_modal_expiration': '2022-09-16T06%3A39%3A57.270Z',
    'language_code': 'en',
    'stockx_selected_locale': 'en',
    'stockx_selected_region': 'AE',
    '_pin_unauth': 'dWlkPVpUbGhZMlJqTURVdFlUQmhNaTAwTnpBeUxXSXpNVFl0WmpFeFpUZzRPVFF5WkdGag',
    'ajs_user_id': 'ac1c19d7-2c10-11ec-9825-124738b50e12',
    'hide_my_vices': 'false',
    '_ga': 'GA1.2.788108403.1627381998',
    '_pxvid': '585cc9e2-407d-11ec-8d1c-64567a454275',
    'tracker_device': '27b681b3-d4ee-46b6-a122-8f55e17dbcd6',
    'stockx_default_watches_size': 'All',
    'ops_banner_id': 'blt055adcbc7c9ad752',
    'ajs_group_id': 'ab_3ds_messaging_eu_web.false%2Cab_aia_pricing_visibility_web.novariant%2Cab_chk_germany_returns_cta_web.true%2Cab_chk_order_status_reskin_web.false%2Cab_chk_place_order_verbage_web.true%2Cab_chk_remove_affirm_bid_entry_web.true%2Cab_chk_remove_fees_bid_entry_web.true%2Cab_citcon_psp_web.true%2Cab_desktop_home_hero_section_web.control%2Cab_home_contentstack_modules_web.variant%2Cab_home_dynamic_content_targeting_web.variant%2Cab_low_inventory_badge_pdp_web.variant_1%2Cab_pirate_recently_viewed_browse_web.true%2Cab_product_page_refactor_web.true%2Cab_recently_viewed_pdp_web.variant_1%2Cab_test_korean_language_web.true%2Cab_web_aa_1103.true',
    'ajs_anonymous_id': 'b9050503-b549-4117-af17-cac10db592f1',
    'stockx_seen_ask_new_info': 'true',
    '__lt__cid': '10d40d29-894a-4333-ba79-89ba26e91495',
    'stockx_device_id': 'web-410547fe-366d-4695-9c14-ec7bb493c03a',
    'stockx_default_collectibles_size': 'All',
    'stockx_default_streetwear_size': 'XL',
    '_tt_enable_cookie': '1',
    '_ttp': '943cb6e4-acfa-4634-ac92-93ef25b9a577',
    '_derived_epik': 'dj0yJnU9YlJyUXhxZG5sVy1ZdDVXS2p4anhZbGJqWjU1R05Zcncmbj1ud042c3BJT0cwa09SOE5ZRkxqaWJnJm09MSZ0PUFBQUFBR0ozZDQ4JnJtPTEmcnQ9QUFBQUFHSjNkNDg',
    'stockx_default_handbags_size': 'All',
    'OptanonAlertBoxClosed': '2022-05-30T07:00:41.776Z',
    'stockx_default_sneakers_size': 'All',
    'stockx_selected_currency': 'USD',
    '_gcl_au': '1.1.625623096.1660208574',
    'rbuid': 'rbos-61bd9993-7bb9-479b-a120-f59e7774fe7c',
    '__pdst': 'b846fcce6a5f4b83a6e5eea55037da64',
    'NA_SAC': 'dT1odHRwcyUzQSUyRiUyRnN0b2NreC5jb20lMkZidXklMkZhZGlkYXMteWVlenktYm9vc3QtMzUwLXR1cnRsZS1kb3ZlLTIwMjIlM0ZkZWZhdWx0QmlkJTNEdHJ1ZXxyPQ==',
    '_gid': 'GA1.2.1180914856.1660545300',
    '_clck': '11tpq9c|1|f41|0',
    'stockx_session': '13149d4b-e4a3-4fc9-8ac7-28b9c59a45c5',
    'stockx_homepage': 'sneakers',
    'QuantumMetricSessionID': '9f945a63a22516d5e9ce16f2a0eec3b6',
    'stockx_product_visits': '578',
    '__cf_bm': 'UOpfReF3Ddmywg.EuXKgdSgmYrJTGQp.FZIv1.wrnQk-1660568637-0-AREffkSyuPIp4hk18Pj7sGIfb3ybdCng8XgOcPvok6+7yrsA8cgJjgiu+ZXNVjMOGJ5Pe2KqQeEwt5kzjQ1vFqc=',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Aug+15+2022+18%3A11%3A05+GMT%2B0500+(Pakistan+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=f03f1052-c1ce-4d1a-bbfc-3c958dc4d2c9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=PK%3BPB',
    'forterToken': 'f97714707aaa44c8bda665516444d4dd_1660569066663_8757_UDF43_13ck',
    '_px3': '49bf3525e8f90601112ca4588e67bbdda2722f96bcd68a1ae36a3ebe805cebec:HaariMLbDKsgkle/UIq7s5eSHgAKHkIeYl1hfEIMUIjiVXHtYpkMU3JMlUaoP07Wvt8SBCJXLAZO1WdM68jx8Q==:1000:F+SFJNo+7eiLzNE4LOPCGQ7yR/5aZXPrMEGN13lerejpslvwW5+29i6iW6S6EtNmZ/H6l7DZGIwmM6ltQs95b37zPLT+xfyeRP48mKuDi2I/8rltghHxPoq3/VD8gApgNNtq17ZnarqghutcIE5/nohkV0y48vYsRDubj0YZxnwhrXetceVVT+j/cinn0c25rQ24nvUFjNkDFaJYZMg6xVSGlb3SwNYiQr9mhIKkQvI=',
    '_gat': '1',
    '_clsk': '61527t|1660569352984|36|0|a.clarity.ms/collect',
    '_pxde': '964079ae0109315d94a0cd62bee7f07884dde79d349880b31054be9671691e48:eyJ0aW1lc3RhbXAiOjE2NjA1NjkzNTIxMTQsImZfa2IiOjB9',
    'IR_9060': '1660569325490%7C0%7C1660569325490%7C%7C',
    'IR_PI': '124d676f-eec6-11eb-84ad-4f7348310cc7%7C1660655725490',
    '_dd_s': 'rum=0&expire=1660570257559',
    'lastRskxRun': '1660569357854',
    '_uetsid': '62c8fa001c6411eda59b5dced0612e69',
    '_uetvid': '0f591ae0eec611eb9ff5fdfee065b825',
}


params = {
    'c': 'ciojs-client-2.29.2',
    'key': 'key_XT7bjdbvjgECO5d8',
    'i': '10fa8973-3324-4013-abaa-596efd9553ad',
    's': '4',
    'num_results_per_page': '25',
    '_dt': '1660729369526',
}

with open('AWSS3accesskeys.txt','r',encoding='utf-8') as file:
    data = file.read().split('\n')
    ACCESS_KEY = data[0]
    SECRET_KEY = data[1]

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        loaded = s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def get_images_from_goat(product):
    S3Images = []
    is360 = True
    images = product['media']['360']
    if len(images) == 0:
        images = product['media']['gallery']
        is360 = False
    if not images or images[0] == None:
        images = [product['media']['imageUrl']]
        is360 = False
    if is360:
        for i in range(1,4):
            imagename = product['styleId'] + f'-{i}.jpg'
            with open(os.path.join(cwd, imagename), 'wb') as handle:
                if i==1:
                    img = images[0].split('?')[0].strip()
                elif i ==2:
                    img = images[17].split('?')[0].strip()
                elif i == 3:
                    img = images[27].split('?')[0].strip()
                response = requests.get(img, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            uploaded = upload_to_aws(os.path.join(cwd, imagename), 'camokicks-storage', imagename)  # upload image from local storage to S3
            if uploaded:
                S3Images.append(f'https://camokicks-storage.s3.amazonaws.com/{imagename}')
                os.remove(os.path.join(cwd, imagename))
    else:
        for i, img in enumerate([v.split('?')[0] for v in images]):
            imagename = product['styleId']+f'-{i}.jpg'
            with open(os.path.join(cwd, imagename), 'wb') as handle:
                response = requests.get(img, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            # wget.download(img, os.path.join(cwd, imagename))  # download image from goat to loacal storage
            uploaded = upload_to_aws(os.path.join(cwd, imagename), 'camokicks-storage', imagename)  # upload image from local storage to S3
            if uploaded:
                S3Images.append(f'https://camokicks-storage.s3.amazonaws.com/{imagename}')
                os.remove(os.path.join(cwd, imagename))
    return S3Images





    # S3Images = []
    # # downloading images from goat
    # goaturl = f'https://ac.cnstrc.com/search/{sku}'
    # rr = requests.get(goaturl, headers=goatheaders, params=params)
    # resp = json.loads(rr.text)
    # urlid = resp['response']['results'][0]['data']['slug']
    # resp2 = requests.get(f'https://www.goat.com/sneakers/{urlid}', headers=headers)
    # resp2 = json.loads(requests.get(
    #     f'https://www.goat.com/_next/data/sQkxGYn1okdMA_cnqY0_h/en-US/sneakers/{urlid}.json?pageSlug=sneakers&productSlug={urlid}',
    #     headers=headers).text)
    # imgs_url = [v['mainPictureUrl'] for v in
    #             resp2['pageProps']['productTemplate']['productTemplateExternalPictures']]
    #
    # for img in imgs_url:
    #     imagename = img.split('/')[-1].split('?')[0]
    #     wget.download(img, os.path.join(cwd, imagename))  # download image from goat to loacal storage
    #     uploaded = upload_to_aws(os.path.join(cwd, imagename), 'camokicks-storage', imagename)  # upload image from local storage to S3
    #     if uploaded:
    #         S3Images.append(f'https://camokicks-storage.s3.amazonaws.com/{imagename}')

CollectionsList = ['Jordan 1 High', 'Jordan 1 Low', 'Jordan 2', 'Jordan 3', 'Jordan 4', 'Jordan 5', 'Jordan 6',
                   'Jordan 7', 'Jordan 8', 'Jordan 9', 'Jordan 10', 'Jordan 11', 'Jordan 12', 'Jordan 13',
                   'Dunk Low', 'Air Force 1', 'Jordan 1 Mid', 'Yeezy', 'Kyrie', 'Lebron', 'Kobe', 'KD',
                   'Blazer', 'Air Max', 'Presto', 'Slide', 'Basketball', 'Men', 'Women', 'Grade School']

Finaldict = []
class stockxdata(scrapy.Spider):
    name = "stockxdata"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_TIMEOUT': 600,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610},
        "ZYTE_SMARTPROXY_ENABLED": True,
        "ZYTE_SMARTPROXY_APIKEY": 'ef2e0ff4f5b24a82a8e715ad869af33a',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': os.path.join(cwd, "cache")
    }

    def start_requests(self):
        # producturl = f'https://stockx.com/api/products/air-jordan-1-mid-greyscale-gs?includes=market&currency=USD'
        # # producturl = f'https://stockx.com/api/products/{urlKey}?includes=market&currency=USD'
        # yield scrapy.Request(url=producturl, headers=headers, callback=self.parse_data)

        brands = ['nike', 'air jordan', 'adidas', 'new balance']
        for brand in brands[:1]:
            for i in range(1, 2):
                url = f'https://stockx.com/api/browse?_tags={brand}&browseVerticals=sneakers&page={i}&propsToRetrieve[][]=id&propsToRetrieve[][]=uuid&propsToRetrieve[][]=childId&propsToRetrieve[][]=title&propsToRetrieve[][]=media.thumbUrl&propsToRetrieve[][]=media.smallImageUrl&propsToRetrieve[][]=urlKey&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=releaseDate&propsToRetrieve[][]=market.lowestAsk&propsToRetrieve[][]=market.highestBid&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=condition&propsToRetrieve[][]=description&propsToRetrieve[][]=shoe&propsToRetrieve[][]=retailPrice&propsToRetrieve[][]=market.lastSale&propsToRetrieve[][]=market.lastSaleValue&propsToRetrieve[][]=market.lastSaleDate&propsToRetrieve[][]=market.bidAskData&propsToRetrieve[][]=market.changeValue&propsToRetrieve[][]=market.changePercentage&propsToRetrieve[][]=market.salesLastPeriod&propsToRetrieve[][]=market.volatility&propsToRetrieve[][]=market.pricePremium&propsToRetrieve[][]=market.averageDeadstockPrice&propsToRetrieve[][]=market.salesThisPeriod&propsToRetrieve[][]=market.deadstockSold&propsToRetrieve[][]=market.lastHighestBidTime&propsToRetrieve[][]=market.lastLowestAskTime&propsToRetrieve[][]=market.salesInformation&facetsToRetrieve[]=%7B%7D'
                yield scrapy.Request(url=url, method='GET', dont_filter=True, cookies=cookies, headers=headers)

    def parse(self, response, **kwargs):
        Jd = json.loads(response.text)
        for product in Jd['Products'][:5]:
            urlKey = product['urlKey']
            # producturl = f'https://stockx.com/api/products/nike-dunk-low-white-black-2021-w?includes=market&currency=USD'
            producturl = f'https://stockx.com/api/products/{urlKey}?includes=market&currency=USD'
            yield scrapy.Request(url=producturl, headers=headers, callback=self.parse_data)

    def parse_data(self, response):
        JData = json.loads(response.text)
        product = JData['Product']
        item = dict()
        size = []
        # for child in (list(product['children'].values())):
        #     size.append(child['shoeSize'])
        # item['size'] = size
        if 'Unisex'.lower() in product['gender'].lower() or 'Child'.lower() in product['gender'].lower() or 'Men'.lower() in product['gender'].lower():
            gender = 'men'
        elif 'Women'.lower() in product['gender'].lower() or 'Female'.lower() in product['gender'].lower():
            gender = 'women'
        else:
            return
        collection = []

        for k in CollectionsList:
            if k.lower() in gender.lower():
                collection.append(k)

        found = False
        for i in CollectionsList:
            if i.lower() in product['title'].lower():
                collection.append(i)
                found = True


        if not found:
            collection.append('other')

        item['collection'] = collection
        # item['units_sold'] = 0
        # item['_id'] = product['id']
        if '(' in product['name']:
            Pname = product['name'].split('(')[0].strip()
            extraName = '(' + product['name'].split('(')[-1].strip()
        else:
            Pname = product['name']
            extraName = ''
        item['name'] = (product['shoe'] + " '" + Pname + "' " + extraName).replace('/','_').replace('\\','_')
        item['description'] = product['description']
        item['brand'] = product['brand']
        if 'men' in gender:
            item['gender'] = 'male'
        elif 'women' in gender:
            item['gender'] = 'female'
        else:
            item['gender'] = gender
        item['images'] = get_images_from_goat(product)

        item['sku'] = product['styleId']
        item['seo_title'] = item['name']
        item['seo_description'] = product['description']
        item['seo_keywords'] = ''
        item['key'] = item['name'].replace(' ','_')
        item['date_created'] = ''
        item['lowest_ask'] = product['market']['lowestAsk']
        item['sku_dewu'] = product['styleId']

        Finaldict.append(item)

    def close(spider, reason):
        with open('sample_json.json', 'w', encoding='utf-8') as filewrite:
            json.dump(Finaldict, filewrite)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(stockxdata)
process.start()
