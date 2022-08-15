import json
import os

import boto3
import requests
import scrapy
import wget
from botocore.exceptions import NoCredentialsError
from scrapy.crawler import CrawlerProcess

cwd = os.getcwd()

headers = {
    "authority": "stockx.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "app-platform": "Iron",
    "app-version": "2022.07.31.05",
    "dnt": "1",
    "referer": "https://stockx.com/sneakers",
    "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

cookies = {
    "stockx_market_country": "KH",
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
    "__pxvid": "87150fcf-0428-11ec-a4f3-0242ac110002",
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
    "NA_SAC": "dT1odHRwcyUzQSUyRiUyRnN0b2NreC5jb20lMkZidXklMkZhaXItam9yZGFuLTEtbWlkLWdyZXlzY2FsZS1ncyUzRmRlZmF1bHRCaWQlM0R0cnVlfHI9",
    "stockx_selected_currency": "USD",
    "stockx_product_visits": "572",
    "__cf_bm": "yPkRPt.STzgZGwK5JwKAQsv_nRuoY9m2MN3t2XNo8J4-1660208568-0-AVunFWOytUX4kBcvZHQZTpMW/zwGLpbvMJf6mvrXGZtFjGFNWEGc8C/QXr0N2c2OKExx813HHO2dcNp4pK02Ypw=",
    "stockx_session": "d0ea10dc-e5b9-418a-88d1-d12cc1e12996",
    "_pxff_idp_c": "1,s",
    "_pxff_fed": "5000",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Aug+11+2022+14%3A02%3A53+GMT%2B0500+(Pakistan+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=f03f1052-c1ce-4d1a-bbfc-3c958dc4d2c9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=PK%3BPB",
    "_gid": "GA1.2.1369666211.1660208574",
    "_gat": "1",
    "forterToken": "f97714707aaa44c8bda665516444d4dd_1660208573521_8757_UDF43_13ck",
    "_gcl_au": "1.1.625623096.1660208574",
    "_px3": "171a9caec8cbdda73ea3259c5bb4efb6a35b7d3867a1b241a46bc094f86bfe4d:naOXPEGsSA4C/PbW8hZrvRArpEPA7DdPIydlwmvySPHnuoz70Pwi8V0Gobv0jNdSGnsf7YyggzqT3nPACvchvg==:1000:syN5nrrv4opUnMH9vl+Q1tTDMU4sIr6K0o/y5i9RdST3XyEVZrVx/Ocas8o2IQMj7mZ/YwJ3aNkrQsICifAt7lzmXxKZwp9zH34zxs3JXELQePm1tly0FcZAIMd64TXM/rAdusGrwXQdjkAB3w+zVL7/0zOOs4POVtYliWeszbu3kKVrDpzqycy7TlCItVZGhGGtqMjajdDg4EP3JhFmdizbiSMCmD/oVFNA55OPtg8=",
    "rbuid": "rbos-61bd9993-7bb9-479b-a120-f59e7774fe7c",
    "_clck": "11tpq9c|1|f3x|0",
    "__pdst": "b846fcce6a5f4b83a6e5eea55037da64",
    "IR_9060": "1660208584833%7C0%7C1660208584833%7C%7C",
    "IR_PI": "124d676f-eec6-11eb-84ad-4f7348310cc7%7C1660294984833",
    "QuantumMetricSessionID": "1dbd9385e7d8f46b9f7d92ad340a5577",
    "_pxde": "2a014ffa47564cfeefbb75b4842b618579acba6f14fc832da482f33d442ba28a:eyJ0aW1lc3RhbXAiOjE2NjAyMDg1ODk1MjQsImZfa2IiOjB9",
    "_uetsid": "636ed830195411eda65f7b7a96eb2570",
    "_uetvid": "0f591ae0eec611eb9ff5fdfee065b825",
    "_dd_s": "rum=2&id=5d9342eb-2117-4699-93dd-bbcb1f527524&created=1660208573177&expire=1660209490787",
    "_clsk": "1tibc6w|1660208592102|2|0|j.clarity.ms/collect",
    "stockx_homepage": "sneakers",
    "lastRskxRun": "1660208592124"
}

goatheaders = {
    "authority": "www.goat.com",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

ACCESS_KEY = 'xxxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


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

image = 'E:\\Project\\pricescraperlk\\scraping\\scraping\\spiders\\895934_01.jpg.jpeg'
class stockxdata(scrapy.Spider):
    name = "stockxdata"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 30,
        'RETRY_HTTP_CODES': [302, 503, 400, 403],
        'Handle_httpstatus_list': [400, 403],
        'ROTATING_PROXY_LIST_PATH': f'{cwd}/proxy.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
        # 'HTTPCACHE_ENABLED': True,
        # 'HTTPCACHE_DIR': 'E:\cache',
        # 'HTTPCACHE_EXPIRATION_SECS': 86400,

    }

    def start_requests(self):
        uploaded = upload_to_aws(image, 'camokicks-storage', '895934_01.jpg.jpeg')
        for i in range(1, 26):
            url = f'https://stockx.com/api/browse?browseVerticals=sneakers&page={i}&propsToRetrieve[][]=id&propsToRetrieve[][]=uuid&propsToRetrieve[][]=childId&propsToRetrieve[][]=title&propsToRetrieve[][]=media.thumbUrl&propsToRetrieve[][]=media.smallImageUrl&propsToRetrieve[][]=urlKey&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=releaseDate&propsToRetrieve[][]=market.lowestAsk&propsToRetrieve[][]=market.highestBid&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=condition&propsToRetrieve[][]=description&propsToRetrieve[][]=shoe&propsToRetrieve[][]=retailPrice&propsToRetrieve[][]=market.lastSale&propsToRetrieve[][]=market.lastSaleValue&propsToRetrieve[][]=market.lastSaleDate&propsToRetrieve[][]=market.bidAskData&propsToRetrieve[][]=market.changeValue&propsToRetrieve[][]=market.changePercentage&propsToRetrieve[][]=market.salesLastPeriod&propsToRetrieve[][]=market.volatility&propsToRetrieve[][]=market.pricePremium&propsToRetrieve[][]=market.averageDeadstockPrice&propsToRetrieve[][]=market.salesThisPeriod&propsToRetrieve[][]=market.deadstockSold&propsToRetrieve[][]=market.lastHighestBidTime&propsToRetrieve[][]=market.lastLowestAskTime&propsToRetrieve[][]=market.salesInformation&facetsToRetrieve[]=%7B%7D'
            yield scrapy.Request(url=url, method='GET', dont_filter=True, cookies=cookies, headers=headers)

    def parse(self, response, **kwargs):
        Jd = json.loads(response.text)
        for product in Jd['Products']:
            urlKey = product['urlKey']
            producturl = f'https://stockx.com/api/products/{urlKey}?includes=market&currency=USD'
            yield scrapy.Request(url=producturl, headers=headers, callback=self.parse_data)

    def parse_data(self, response):
        JData = json.loads(response.text)
        product = JData['Product']
        item = dict()
        size = []
        for child in (list(product['children'].values())):
            size.append(child['shoeSize'])
        item['size'] = size
        item['collections'] = [product['listingType'], product['secondaryCategory']]
        item['_id'] = product['id']
        item['name'] = product['name']
        item['description'] = product['description']
        item['brand'] = product['brand']
        item['gender'] = product['gender']
        item['sku'] = product['styleId']
        #downloading images from goat
        goaturl = f'https://www.goat.com/_next/data/sQkxGYn1okdMA_cnqY0_h/en-US/search.json?query={product["styleId"]}'
        rr = requests.get(goaturl, headers=goatheaders)
        resp = json.loads(rr.text)
        urlid = resp['pageProps']['constructorResponse']['response']['results'][0]['data']['slug']
        resp2 = json.loads(requests.get(
            f'https://www.goat.com/_next/data/sQkxGYn1okdMA_cnqY0_h/en-US/sneakers/{urlid}.json?pageSlug=sneakers&productSlug={urlid}',
            headers=headers).text)
        imgs_url = [v['mainPictureUrl'] for v in
                    resp2['pageProps']['productTemplate']['productTemplateExternalPictures']]

        S3Images = []
        for img in imgs_url:
            imagename = img.split('/')[-1].split('?')[0]
            wget.download(img,os.path.join(cwd, imagename)) #download image from goat to loacal storage
            uploaded = upload_to_aws(os.path.join(cwd, imagename), 'camokicks-storage', imagename)#upload image from local storage to S3
            if uploaded:
                S3Images.append(f'https://camokicks-storage.s3.amazonaws.com/{imagename}')

        item['images'] = S3Images

        item['seo_title'] = product['title']
        item['seo_description'] = product['description']
        item['seo_keywords'] = ''
        item['key'] = ''
        item['date_created'] = ''
        item['date_created'] = ''
        item['lowest_ask'] = product['market']['lowestAsk']
        item['sku_dewu'] = product['styleId']


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(stockxdata)
process.start()
