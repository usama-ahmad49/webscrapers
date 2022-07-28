import requests
import urllib.parse

headers = {
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'bcookie="v=2&4de788bb-658b-4f3d-8e88-2200857f0452"; li_sugr=ef549021-3740-4f7d-b75b-abb56688efc0; lang=v=2&lang=en-us; bscookie="v=1&20201201111614bb99c89d-244b-4008-88f8-fab7e34521d9AQGWadwWW7zaNxwUeTFY73xdFZTi025W"; JSESSIONID="ajax:5723224059102653570"; liap=true; li_gc=MTswOzE2MjczNjgzMjc7MjswMjH2vV7kZFHCCC+CW6rYSi/Ts0/hUVTidYiYREgmrynPsw==; li_theme=light; li_theme_set=app; _guid=47c7f7b0-4f51-4cf5-8d99-a3523d787217; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=86326393277335660000688205653805587688; li_at=AQEDAR6-qv4EMeQ5AAABeI3GcFcAAAGBi8HtsE0Ah9qyzUVa4ZhPO0-eCyfB2Ufj-o6p-olFT3WN1J7aLBVMm_Uf5XmjzZG3J1T1TlN6kYSbngiT6KQskrYp3EkyeZ-C9IOgP9Q-9jtof_n8F43Irsi4; timezone=Asia/Karachi; _gcl_au=1.1.1353431559.1655363729; AnalyticsSyncHistory=AQK_HEo7eGP9IwAAAYGBUK_0S-7aPgtmgPoP6zm4CTHPRWTuRQyrJW-XSYkPl72TW7RTMkEdvacwiaDm9oU_qw; lms_ads=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; lms_analytics=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; sdsc=22%3A1%2C1655731995163%7ECONN%2C0iqoii7lXWYU2r0n3PLzjK8SIzGY%3D; UserMatchHistory=AQJOcz3TyDGLLQAAAYGFDxxKMAZEu_sk08s0DOxHgXjUqrfXHk1xbjgAdHsY8pSTWIX6wGxVqDD3ZBGTiqdsbQ36fh4ysN1ejuOQyD3TAlz_K5QmS4Zef1fuqAbobEOvgjGHjgqABG48T3TBmH1kAEH9cCNlQLBwbnJUbjopNKo_eK8gMh3nOfbpjzVFmPS1yvsMHwJ2fbH31K3448dODZgusJmivotYw-hZo08CbKOi9yGcbx9FcsmPdFk1gmbmn74U6-XXARbeGcJRhbukxLgcYjFzc-o6gBBhd6k; lidc="b=TB94:s=T:r=T:a=T:p=T:g=2812:u=179:x=1:i=1655794773:t=1655818347:v=2:sig=AQFsux5QZN7kozhkWpai60PbVvXfWVs-"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19164%7CMCMID%7C85755271742574248910667606254403563299%7CMCAAMLH-1656399575%7C3%7CMCAAMB-1656399575%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1655801975s%7CNONE%7CMCCIDH%7C1294912360%7CvVersion%7C5.1.1; li_mc=MTsyMTsxNjU1Nzk0OTcwOzE7MDIxO3n8pMGmxEvHGiIPjjt1t2qnuNRhzlEugvNEcIhh48A=',
    'csrf-token': 'ajax:5723224059102653570',
    'dnt': '1',
    'referer': 'https://www.linkedin.com/search/results/all/?keywords=i%20am%20looking%20for%20a%20job&origin=TYPEAHEAD_HISTORY&position=0&searchId=b6a092ef-0337-40d8-b4ea-a1983c8a55f7&sid=I6p',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'x-li-lang': 'en_US',
    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_content;WG3ec0LoR4mYe7ohlg0few==',
    'x-li-track': '{"clientVersion":"1.10.6174","mpVersion":"1.10.6174","osName":"web","timezoneOffset":5,"timezone":"Asia/Karachi","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
    'x-restli-protocol-version': '2.0.0',
}

keywords = "מחפשת סטודנט משרת"
word = keywords.encode('UTF-8')
company_link = 'https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-155&origin=GLOBAL_SEARCH_HEADER&q=all&query=(keywords:'+keywords+',flagshipSearchIntent:SEARCH_SRP,queryParameters:(resultType:List(CONTENT)))&start=0'

with requests.session() as s:
    s.cookies['li_at'] = "AQEDATxT0j0Fkks8AAABgYUebmgAAAGBqSryaFYAJAizxhNvzCXP-gX_yiFXlRXmzd4jAhOVM8dBGWzThk6GXpcz4P6WASmZqaR-yJ-OpWT2y91JytQGdb8h4xegbQzxcF59LT2PmS2RX4aBxmNSFIcr"
    s.cookies["JSESSIONID"] = "ajax:0722808039379375364"
    s.headers = headers
    s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
    response = s.get(company_link)
    response_dict = response.json()
    print(response_dict)