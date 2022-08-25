import json
import os
import re
import boto3
import requests
import scrapy
from botocore.exceptions import NoCredentialsError
from scrapy.crawler import CrawlerProcess

cwd = os.getcwd()
headers = {
    "authority": "stockx.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "app-platform": "Iron",
    "app-version": "2022.08.14.05",
    "dnt": "1",
    "referer": "https://stockx.com/retro-jordans/air-jordan-5?size_types=men",
    "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    'X-Crawlera-Max-Retries': '1',
    'X-Crawlera-Profile': 'desktop',
    'X-Crawlera-Cookies': 'discard',
    'X-Crawlera-Region': 'ca'
}
cookies = {
    "stockx_market_country": "PK",
    "_ga": "GA1.2.788108403.1627381998",
    "pxcts": "0e9c4630-eec6-11eb-8f35-456c805b484e",
    "_scid": "d66f0315-e66c-43f7-9088-cb913be1d684",
    "product_page_affirm_callout_enabled_web": "false",
    "riskified_recover_updated_verbiage": "true",
    "home_vertical_rows_web": "true",
    "_px_f394gi7Fvmc43dfg_user_id": "MTA0OTU5ZjEtZWVjNi0xMWViLTkzMWQtNzU0NDc2NWQ2YjUy",
    "QuantumMetricUserID": "d09c7fd3ca35f4883252442e93c26ffb",
    "rskxRunCookie": "0",
    "rCookie": "o5z2ngw5qrkce8yubt0e7tkrlx854q",
    "IR_gbd": "stockx.com",
    "_rdt_uuid": "1627382004357.08170ccd-84e5-4727-b809-30b9e8d7868b",
    "__ssid": "3ff3af1fd98b9b60409658d135799ec",
    "_ts_yjad": "1629827453266",
    "stockx_preferred_market_activity": "sales",
    "stockx_dismiss_modal_set": "2021-09-16T06%3A39%3A57.270Z",
    "stockx_dismiss_modal": "true",
    "stockx_dismiss_modal_expiration": "2022-09-16T06%3A39%3A57.270Z",
    "language_code": "en",
    "stockx_selected_locale": "en",
    "stockx_selected_region": "AE",
    "_pin_unauth": "dWlkPVpUbGhZMlJqTURVdFlUQmhNaTAwTnpBeUxXSXpNVFl0WmpFeFpUZzRPVFF5WkdGag",
    "ajs_user_id": "ac1c19d7-2c10-11ec-9825-124738b50e12",
    "hide_my_vices": "false",
    "_pxvid": "585cc9e2-407d-11ec-8d1c-64567a454275",
    "tracker_device": "27b681b3-d4ee-46b6-a122-8f55e17dbcd6",
    "stockx_default_watches_size": "All",
    "ops_banner_id": "blt055adcbc7c9ad752",
    "ajs_group_id": "ab_3ds_messaging_eu_web.false%2Cab_aia_pricing_visibility_web.novariant%2Cab_chk_germany_returns_cta_web.true%2Cab_chk_order_status_reskin_web.false%2Cab_chk_place_order_verbage_web.true%2Cab_chk_remove_affirm_bid_entry_web.true%2Cab_chk_remove_fees_bid_entry_web.true%2Cab_citcon_psp_web.true%2Cab_desktop_home_hero_section_web.control%2Cab_home_contentstack_modules_web.variant%2Cab_home_dynamic_content_targeting_web.variant%2Cab_low_inventory_badge_pdp_web.variant_1%2Cab_pirate_recently_viewed_browse_web.true%2Cab_product_page_refactor_web.true%2Cab_recently_viewed_pdp_web.variant_1%2Cab_test_korean_language_web.true%2Cab_web_aa_1103.true",
    "ajs_anonymous_id": "b9050503-b549-4117-af17-cac10db592f1",
    "stockx_seen_ask_new_info": "true",
    "__lt__cid": "10d40d29-894a-4333-ba79-89ba26e91495",
    "stockx_device_id": "web-410547fe-366d-4695-9c14-ec7bb493c03a",
    "stockx_default_collectibles_size": "All",
    "stockx_default_streetwear_size": "XL",
    "_tt_enable_cookie": "1",
    "_ttp": "943cb6e4-acfa-4634-ac92-93ef25b9a577",
    "_derived_epik": "dj0yJnU9YlJyUXhxZG5sVy1ZdDVXS2p4anhZbGJqWjU1R05Zcncmbj1ud042c3BJT0cwa09SOE5ZRkxqaWJnJm09MSZ0PUFBQUFBR0ozZDQ4JnJtPTEmcnQ9QUFBQUFHSjNkNDg",
    "stockx_default_handbags_size": "All",
    "OptanonAlertBoxClosed": "2022-05-30T07:00:41.776Z",
    "stockx_default_sneakers_size": "All",
    "stockx_selected_currency": "USD",
    "_gcl_au": "1.1.625623096.1660208574",
    "rbuid": "rbos-61bd9993-7bb9-479b-a120-f59e7774fe7c",
    "__pdst": "b846fcce6a5f4b83a6e5eea55037da64",
    "NA_SAC": "dT1odHRwcyUzQSUyRiUyRnN0b2NreC5jb20lMkZidXklMkZhZGlkYXMteWVlenktYm9vc3QtMzUwLXR1cnRsZS1kb3ZlLTIwMjIlM0ZkZWZhdWx0QmlkJTNEdHJ1ZXxyPQ==",
    "stockx_homepage": "sneakers",
    "stockx_product_visits": "590",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Aug+24+2022+14%3A49%3A21+GMT%2B0500+(Pakistan+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=f03f1052-c1ce-4d1a-bbfc-3c958dc4d2c9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=PK%3BPB",
    "_gid": "GA1.2.1486831436.1661334562",
    "forterToken": "f97714707aaa44c8bda665516444d4dd_1661334561221_8757_UDF43_13ck",
    "_px3": "469151d02b19bd8df5252c9d0e2c35e7b8e67f0cc69caad703344131ac86a827:8JPOMfp4TZMge9a3PG4OjA3VjkfjpwGkFcjeA9xaraseW5aEfclaiiduj/sEdJykBY27I/9DiejwGFLiy4vYsg==:1000:Si5QhuDbEsx027c2GAG1qdjh6RULSBRrV6FnDZ6DAMnR52dygWo/FbXZpFaQbBlSALpC1we17L+P4i6NIHMJxZPuyjdh4vW+8TlSvbL2xC7JjlPN9dGmOmHCBfY6+ZibNIgxq6lPkfl+Av1ihO/BRHCKJ0FRRObqgrnDBp17L60h1WH6nX9G6adB4uYu7m9yOwnzVNWNSlbPLEguL86BZzEN/3jslqadUbmZ0JIPUS4=",
    "_clck": "11tpq9c|1|f4b|0",
    "stockx_session": "d1afe504-4bbf-4e27-8734-c109954189f9",
    "__cf_bm": "Ne.7QgDTmJX3LSCk3kiS9MzH.33.cpYbzMvsa_sm1fY-1661408587-0-AVJv0BvYe3uSGRZjuFgf4pt/iPCWLloQEzZ0mKG08bfinsr5D2ahDXK8RTyWVKlRbmcYcJjfnw7zwofYo5bEayM=",
    "_uetsid": "07e03c10239211ed8b4b77178138f411",
    "_uetvid": "0f591ae0eec611eb9ff5fdfee065b825",
    "_clsk": "14ryk9a|1661408726487|9|0|j.clarity.ms/collect",
    "_pxde": "5124c4cb8fa1edc8159693a3d77d81d3802911e5645b69dbcc0d8f019ef8b01d:eyJ0aW1lc3RhbXAiOjE2NjE0MDg3MjYzMjksImZfa2IiOjB9",
    "IR_9060": "1661408634527%7C0%7C1661408634527%7C%7C",
    "IR_PI": "124d676f-eec6-11eb-84ad-4f7348310cc7%7C1661495034527",
    "_dd_s": "rum=0&expire=1661409817546",
    "_gat": "1",
    "lastRskxRun": "1661408917788"
}

params = {
    'c': 'ciojs-client-2.29.2',
    'key': 'key_XT7bjdbvjgECO5d8',
    'i': '10fa8973-3324-4013-abaa-596efd9553ad',
    's': '4',
    'num_results_per_page': '25',
    '_dt': '1660729369526',
}

with open('AWSS3accesskeys.txt', 'r', encoding='utf-8') as file:
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
        for i in range(1, 4):
            imagename = product['styleId'] + f'-{i}.jpg'
            with open(os.path.join(cwd, imagename), 'wb') as handle:
                if i == 1:
                    img = images[0].split('?')[0].strip()
                elif i == 2:
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
            imagename = product['styleId'] + f'-{i}.jpg'
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


CollectionsList = ['Jordan 1 High', 'Jordan 1 Mid', 'Jordan 1 Low', 'Jordan 2', 'Jordan 3', 'Jordan 4', 'Jordan 5', 'Jordan 6',
                   'Jordan 7', 'Jordan 8', 'Jordan 9', 'Jordan 10', 'Jordan 11', 'Jordan 12', 'Jordan 13',
                   'Dunk Low', 'Air Force 1', 'Yeezy', 'Kyrie', 'Lebron', 'Kobe', 'KD',
                   'Blazer', 'Air Max', 'Presto', 'Slide', 'Basketball', 'Men', 'Women', 'Grade School']

tagsToSearch = ['adidas', 'new balance', 'nike', 'air jordan', 'one,air jordan', 'two,air jordan', 'three,air jordan', 'four,air jordan', 'five,air jordan', 'six,air jordan', 'seven,air jordan', 'eight,air jordan',
                'nine,air jordan', 'ten,air jordan', 'eleven,air jordan', 'twelve,air jordan', 'thirteen,air jordan', 'dunk,nike', 'air force,nike', 'yeezy,nike', 'lebron,nike',
                'kobe,nike', 'kd,nike', 'blazer,nike', 'air max,nike', 'presto,nike', 'nike basketball,nike']

Finaldict = []
ignoreKeyword = ['(PS)', '(I)', '(INFANT)', '(INFANTS)', '(KIDS)', '(TD)']
with open('ALready_Existing_UrlKeys.txt', 'r', encoding='utf-8') as KeysFile:
    ALready_Existing_UrlKeys = KeysFile.read().split('\n')
New_UrlKeys_Found = []


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
        'HTTPCACHE_DIR': os.path.join(cwd, "cache"),
        # 'RETRY_TIMES': 20,
        # 'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408]
    }

    def start_requests(self):
        # producturl = f'https://stockx.com/api/products/adidas-yeezy-boost-350-v2-core-black-red-2017?includes=market&currency=USD'
        # # producturl = f'https://stockx.com/api/products/{urlKey}?includes=market&currency=USD'
        # yield scrapy.Request(url=producturl, headers=headers, callback=self.parse_data)

        for gender in ['men', 'women', 'child']:
            for tag in tagsToSearch:
                for i in range(1, 26):
                    url = f'https://stockx.com/api/browse?_tags={tag}&browseVerticals=sneakers&page={i}&gender={gender}&propsToRetrieve[][]=id&propsToRetrieve[][]=uuid&propsToRetrieve[][]=childId&propsToRetrieve[][]=title&propsToRetrieve[][]=media.thumbUrl&propsToRetrieve[][]=media.smallImageUrl&propsToRetrieve[][]=urlKey&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=releaseDate&propsToRetrieve[][]=market.lowestAsk&propsToRetrieve[][]=market.highestBid&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=condition&propsToRetrieve[][]=description&propsToRetrieve[][]=shoe&propsToRetrieve[][]=retailPrice&propsToRetrieve[][]=market.lastSale&propsToRetrieve[][]=market.lastSaleValue&propsToRetrieve[][]=market.lastSaleDate&propsToRetrieve[][]=market.bidAskData&propsToRetrieve[][]=market.changeValue&propsToRetrieve[][]=market.changePercentage&propsToRetrieve[][]=market.salesLastPeriod&propsToRetrieve[][]=market.volatility&propsToRetrieve[][]=market.pricePremium&propsToRetrieve[][]=market.averageDeadstockPrice&propsToRetrieve[][]=market.salesThisPeriod&propsToRetrieve[][]=market.deadstockSold&propsToRetrieve[][]=market.lastHighestBidTime&propsToRetrieve[][]=market.lastLowestAskTime&propsToRetrieve[][]=market.salesInformation&facetsToRetrieve[]=%7B%7D'
                    # url = f'https://stockx.com/api/browse?_tags={brand}&browseVerticals=sneakers&page={i}&propsToRetrieve[][]=id&propsToRetrieve[][]=uuid&propsToRetrieve[][]=childId&propsToRetrieve[][]=title&propsToRetrieve[][]=media.thumbUrl&propsToRetrieve[][]=media.smallImageUrl&propsToRetrieve[][]=urlKey&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=releaseDate&propsToRetrieve[][]=market.lowestAsk&propsToRetrieve[][]=market.highestBid&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=condition&propsToRetrieve[][]=description&propsToRetrieve[][]=shoe&propsToRetrieve[][]=retailPrice&propsToRetrieve[][]=market.lastSale&propsToRetrieve[][]=market.lastSaleValue&propsToRetrieve[][]=market.lastSaleDate&propsToRetrieve[][]=market.bidAskData&propsToRetrieve[][]=market.changeValue&propsToRetrieve[][]=market.changePercentage&propsToRetrieve[][]=market.salesLastPeriod&propsToRetrieve[][]=market.volatility&propsToRetrieve[][]=market.pricePremium&propsToRetrieve[][]=market.averageDeadstockPrice&propsToRetrieve[][]=market.salesThisPeriod&propsToRetrieve[][]=market.deadstockSold&propsToRetrieve[][]=market.lastHighestBidTime&propsToRetrieve[][]=market.lastLowestAskTime&propsToRetrieve[][]=market.salesInformation&facetsToRetrieve[]=%7B%7D'
                    yield scrapy.Request(url=url, method='GET', headers=headers)

    def parse(self, response, **kwargs):
        Jd = json.loads(response.text)
        for product in Jd['Products']:
            urlKey = product['urlKey']
            # producturl = f'https://stockx.com/api/products/nike-dunk-low-white-black-2021-w?includes=market&currency=USD'
            producturl = f'https://stockx.com/api/products/{urlKey}?includes=market&currency=USD'
            yield scrapy.Request(url=producturl, headers=headers, callback=self.parse_data)

    def parse_data(self, response):
        JData = json.loads(response.text)
        product = JData['Product']

        if product['urlKey'] in ALready_Existing_UrlKeys:
            return
        else:
            New_UrlKeys_Found.append(product['urlKey'])

        item = dict()
        # size = []
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
            col = ' '.join([v for v in i.lower().split() if v in product['title'].lower()])
            if col.title() in CollectionsList:
                collection.append(i)
                found = True
            # if i.lower() in product['title'].lower():
            #     collection.append(i)
            #     found = True

        if not found:
            collection.append('other')

        item['collection'] = collection
        # item['units_sold'] = 0
        # item['_id'] = product['id']
        if '(' in product['name']:
            Pname = product['name'].split('(')[0].strip()
            extraName = '(' + product['name'].split('(')[-1].strip().split('/')[-1]
        else:
            Pname = product['name']
            extraName = ''
        if extraName in ignoreKeyword:
            return
        item['name'] = (product['shoe'] + " '" + Pname + "' " + extraName).strip()
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
        item['key'] = item['name'].replace(' ', '_')
        item['date_created'] = ''
        item['lowest_ask'] = product['market']['lowestAsk']
        item['sku_dewu'] = product['styleId']

        Finaldict.append(item)
        with open(f"{product['styleId']}_json.json", 'w', encoding='utf-8') as filewrite:
            json.dump(item, filewrite)

    def close(spider, reason):
        with open('final_Product_json.json', 'w', encoding='utf-8') as filewrite:
            json.dump(Finaldict, filewrite)

        with open('ALready_Existing_UrlKeys.txt', 'a', encoding='utf-8') as AEUK:
            for key in New_UrlKeys_Found:
                AEUK.write(key + '\n')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(stockxdata)
process.start()
