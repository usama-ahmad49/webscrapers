import scrapy
from scrapy.crawler import CrawlerProcess



headers = {
    "authority": "www.tiktok.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.tiktok.com/@readingslay",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

cookies = {
    "tt_csrf_token": "n70C4neB-F8jun4VjmD1TTTPPClhBrtUZ3vE",
    "tiktok_webapp_theme": "light",
    "__tea_cache_tokens_1988": "{%22_type_%22:%22default%22%2C%22user_unique_id%22:%227186973713463477762%22%2C%22timestamp%22:1673347734479}",
    "csrf_session_id": "5544d64c7071bb727ba59f80c38918f1",
    "s_v_web_id": "verify_lcq41asm_QHAtV9Cz_IYk7_4tdF_8pXn_8s78gRYxXYBD",
    "tt_chain_token": "11433j5oRC0NEab2KSbMNg==",
    "_abck": "D935D5980CB0AA9C67E120DDE2153EC1~0~YAAQBeVdbuQpwhOFAQAA5AbppAnRRtBtge56lGjtbluEWdNgD9B1qyZQhHHaMuusczdneUZXvjXl3jsj5u3EE4t48iuro3XErTe9HNIfmCC8JsRXA3/SV3nEgaEz71ZDrQ5+D/ye95JE8fP8TPDyaytf7EJ1ZcTfaSBTujyxtcO0RvlZae3ROxcrrIbUW48obcce7gLfHnLVMfGdDh+TMA56VuJutp2dWgCe3pTKv1Q/RTakWoV0o889Nsx6MWq/bCPTgBkUuDKLRqaqO+rhZDkh3/AtNnSQHRZLSJ2GY4bm5wdIcQsEikouqRSZVWFIdlwBGM8Addfxg2VWCCnh0AIHjeQSlE6A3YhDgpw0zcbg3SkWkvmgs263p/f0YcdooWr/CGDlKVJMYaqVyKo8jEd/GyXcsDI7~-1~-1~-1",
    "bm_sz": "2C3F601130C1EF7431773B3D8BD17FC6~YAAQBeVdbucpwhOFAQAA5AbppBL42LSnpKeK5i6/y35ltetvJslKSxRy0q2Q4CPAoO+qPd/DvGnRMxek6+DuoDKuoQ+0kpJIelN3be8FeyLQGdrm1aSd/5VT9s94gEKPOKfNlfDI/zHmsfc4sOSP1tg6/UT7e5M4aBHKyQ6Gipz1VQ5nj8y8IMhZ/w4v4JiW0PEV2H1r2GlE7rXBRKlTmO6OSp7eCJrhqzUmdKrqlSSUgEgWUGL7qvZTCkGyf9LLpeNHWdAehYngDYao19JXIA9g1m9WXwLSi/9h0lc6bm9WfEY=~4536630~4342328",
    "ak_bmsc": "756E595D38C46190D50383FF34FA0AEE~000000000000000000000000000000~YAAQBeVdbuspwhOFAQAALxHppBIKEyr/YK8b9nJ2l58/qtVayXMYo23rN4OtDSohehXBah1XmWivUDqe9zr890DZiVgkV8eBjkE/owl7yQpimESeN4bgtOe+XWEp6212HgEoPzh7uoJVukNrCAcXA9//Wdo3eTHAzprlAjk2V+dWOFOPo+C9FUdsYcp9pqTl2DwA4IUdc/cKAxX4dxKawiUfwLTGcBo2OYNwX0itioWvZnpTiJLldBTPwvwA5D1s8j4DjejBrhATVRvpx6aVbwBD+XZ5pxqtJo+WX8ry6KWLul6x2XiTWr4MOVOUZOWyO5MdwIm7S8+UMyBCpMHLuxtzUJf9NXg3o+V2Gtm19vm9x2OrG8vu3bEaT5zEf777Dox1izlSLhXooLjevkI7VtpkGbtabneADzRniJk9zfEjE5gCKk3U7hU+5LKtbXwRLfFUNVQ3QvqkI3aIUAScYHhU0+LsLQYcLg/uTlEX6UhmcmDt07Y6ljKiMcE=",
    "ttwid": "1%7Cq6s_KGe3aeuXOGL_pkcvejowSs63vAgfekQRrZw59OY%7C1673509722%7Cdf23f7d0579f52c02a57c574824d9850328bd3ce8fab84ded15ee279383a90ad",
    "msToken": "0iTb91eiP8EOMNTWwQ6MrlgW4HtLToInzjwzNAlvQDVAOOJspyPOmglDxjzC8pZJXHhxLrqjH5-r8hpUd2DqUOSVVGvncI50jCNpWFn69sNsgY5LiVkwok5jKp28g_bpB3pC6E19GoE2KjA=",
    "bm_sv": "0BB29991A2BD8B72B69C0A633018B9F0~YAAQDeldbnoxHCuFAQAAQ3YBpRL3O/Q4G2yj/nfZrYIoLvEmqOox/Wr2D6fL2JvFEb3I8GIvW5Lp+9HdUGvnCNEoHWpyFgKpkF7RUUYruPjc7BpMgYCwUL+L3jAxw/BeR7zMDMV7Tahl/ZDIClaoJWTe9f7b1kL5Tr+868HvyMkueiRB5sogVvvBYDFQ4SV1KhgP2C85D6ynf5Hs/LU4YovfatHxYN0TLWVMxyzlhh0AYD7YBkW7Bo8zZ0+rbDkARQ==~1"
}

class test(scrapy.Spider):
    name = 'test'
    def start_requests(self):
        url = 'https://www.tiktok.com/api/user/detail/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=1&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F109.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7186973713463477762&device_platform=web_pc&focus_state=true&from_page=user&history_len=2&is_fullscreen=false&is_page_visible=true&language=en&os=windows&priority_region=&referer=&region=PK&screen_height=1080&screen_width=1920&secUid=MS4wLjABAAAAxaI5DwKsNd2fIQE_GOt5Q_RDKDQMGqIpgNocLaAqXSrh65ALBijLxPeJhBk80Q2-&tz_name=Asia%2FKarachi&uniqueId=readingslay&verifyFp=verify_lcq41asm_QHAtV9Cz_IYk7_4tdF_8pXn_8s78gRYxXYBD&webcast_language=en&msToken=tOKqxlw0ugps5M_ybddtOAfC_5pXI2PDtWvxoEWNAFqLQ9_X_sH1yQNx0ZbXyutI2JrI95zWgpSOC5RLTSUwM8-jnYAMYoGX3IyG4podBUtNCIChwMaBwUX5zuCf9o_ltt3hH-PWKDfH4XU=&X-Bogus=DFSzswVOl2vAN9ILSDzcz5YklTXv&_signature=_02B4Z6wo00001Va5qHwAAIDAiM.w2F6oI5VWuazAADYVa0'
        yield scrapy.Request(url=url ,cookies=cookies, headers=headers,)
    def parse(self, response, **kwargs):
        pass

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
process.crawl(test)
process.start()