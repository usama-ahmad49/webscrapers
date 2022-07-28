import json
import time

import requests
import urllib.parse
from seleniumwire import webdriver
import csv
import scrapy
headers = {
    'authority': 'www.linkedin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'bcookie="v=2&4de788bb-658b-4f3d-8e88-2200857f0452"; li_sugr=ef549021-3740-4f7d-b75b-abb56688efc0; lang=v=2&lang=en-us; bscookie="v=1&20201201111614bb99c89d-244b-4008-88f8-fab7e34521d9AQGWadwWW7zaNxwUeTFY73xdFZTi025W"; JSESSIONID="ajax:5723224059102653570"; liap=true; li_gc=MTswOzE2MjczNjgzMjc7MjswMjH2vV7kZFHCCC+CW6rYSi/Ts0/hUVTidYiYREgmrynPsw==; li_theme=light; li_theme_set=app; _guid=47c7f7b0-4f51-4cf5-8d99-a3523d787217; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=86326393277335660000688205653805587688; timezone=Asia/Karachi; _gcl_au=1.1.1353431559.1655363729; AnalyticsSyncHistory=AQK_HEo7eGP9IwAAAYGBUK_0S-7aPgtmgPoP6zm4CTHPRWTuRQyrJW-XSYkPl72TW7RTMkEdvacwiaDm9oU_qw; lms_ads=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; lms_analytics=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; sdsc=22%3A1%2C1655731995163%7ECONN%2C0iqoii7lXWYU2r0n3PLzjK8SIzGY%3D; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19164%7CMCMID%7C85755271742574248910667606254403563299%7CMCAAMLH-1656410748%7C3%7CMCAAMB-1656410748%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1655813148s%7CNONE%7CMCCIDH%7C1294912360%7CvVersion%7C5.1.1; li_at=AQEDAR6-qv4EMeQ5AAABeI3GcFcAAAGBs9N1iU0AtBALRINInc9ZngO9_7lSu_QM45-hGf8yFhSjD1ECG84CKwCqZymPAo1WHUCtJzQsemIM4s8tV8W1DdBhmDtDg6Dlcjy3dFWqwprdmyszEbgdfmtB; UserMatchHistory=AQKN15BffOwjQgAAAYGQMuqLKLLXuOJstdi3a4D6fH1sdSQoKOLzTSB_yhlMGhuIT1JpuZak5SXxV_6zbAmt5J5gJfK4KpsrlbbIAa-RZqk3QJ45CfOFo8HbL4I1dJ2gqqY6oNMI780r6LmeN9IOWiGQ7QaYyEIJvgqlk_r14PUhfWKhzHmQ-scq7fM6Oad931QVdypKECjGiRWn0LQWGuYdYsH6nWvGB-jjZjDBRcu4Yb_UC6uFqtGF0Kqu07NpPAyg0ji7jMtMtlbKyPQ0ayGW1lrFkVSNrTxY-Hc; lidc="b=TB94:s=T:r=T:a=T:p=T:g=2815:u=180:x=1:i=1655981666:t=1656060988:v=2:sig=AQFijol0ZLhv5LSUpRxmt2Jjqo7iO-n7"; li_mc=MTsyMTsxNjU1OTgyNzQ2OzE7MDIxcgN+hEjZ6ZZ2jkUmBwJQM7o0WovQFx/Es74ahkXpJw8=',
    'dnt': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}
headers2 = {
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'bcookie="v=2&4de788bb-658b-4f3d-8e88-2200857f0452"; li_sugr=ef549021-3740-4f7d-b75b-abb56688efc0; lang=v=2&lang=en-us; bscookie="v=1&20201201111614bb99c89d-244b-4008-88f8-fab7e34521d9AQGWadwWW7zaNxwUeTFY73xdFZTi025W"; JSESSIONID="ajax:5723224059102653570"; liap=true; li_gc=MTswOzE2MjczNjgzMjc7MjswMjH2vV7kZFHCCC+CW6rYSi/Ts0/hUVTidYiYREgmrynPsw==; li_theme=light; li_theme_set=app; _guid=47c7f7b0-4f51-4cf5-8d99-a3523d787217; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=86326393277335660000688205653805587688; timezone=Asia/Karachi; _gcl_au=1.1.1353431559.1655363729; AnalyticsSyncHistory=AQK_HEo7eGP9IwAAAYGBUK_0S-7aPgtmgPoP6zm4CTHPRWTuRQyrJW-XSYkPl72TW7RTMkEdvacwiaDm9oU_qw; lms_ads=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; lms_analytics=AQGc65OeiYjmVAAAAYGBUL2PN4LwhHbGvOCMRQS2_GiiQQGxeVamp0o_R7TRU7Jva-58v-NDKcHXzvJ7m2MAZ5CIjH2hbvjC; sdsc=22%3A1%2C1655731995163%7ECONN%2C0iqoii7lXWYU2r0n3PLzjK8SIzGY%3D; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19164%7CMCMID%7C85755271742574248910667606254403563299%7CMCAAMLH-1656410748%7C3%7CMCAAMB-1656410748%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1655813148s%7CNONE%7CMCCIDH%7C1294912360%7CvVersion%7C5.1.1; li_at=AQEDAR6-qv4EMeQ5AAABeI3GcFcAAAGBs9N1iU0AtBALRINInc9ZngO9_7lSu_QM45-hGf8yFhSjD1ECG84CKwCqZymPAo1WHUCtJzQsemIM4s8tV8W1DdBhmDtDg6Dlcjy3dFWqwprdmyszEbgdfmtB; li_mc=MTsyMTsxNjU1OTc0NTg4OzE7MDIxeABgj4luXsYmDXxht1EguL9wROe2n7DeNROvpjRIPUw=; UserMatchHistory=AQKqKkG4YEzooAAAAYGPyFRLm3ezDd4erpTlajYRxx_k7bxs--Kv9rkmJ-IlkTaSy6bo0yTtzh7C_GVkjJsTH3Ed2Ciq0U2GWjl-78DG-Z1p-w90DAPsiOSV88N4Q6QMmEnyhJG2IgiGv-izhwstkoZzctWmvPNWHvyb0fjKmxsw5tpRghmVn8z6xaixSsDYMBOfPltJZera_T-twJm0RoOybsAzSH21fO6S1qeRvER7dA2l53M8kM-o2N1lnqQMVbNSxrnHKxbko8z3zAZn6SsnzZjWB__hmYJC8qY; lidc="b=TB94:s=T:r=T:a=T:p=T:g=2815:u=180:x=1:i=1655974680:t=1656060988:v=2:sig=AQHOoK8eQkdazgxwFekxOLjjlBp1heb4"',
    'csrf-token': 'ajax:5723224059102653570',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.linkedin.com/in/jonsquire/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'x-li-lang': 'en_US',
    'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;CwVn4NrqRF6R+h/Cj3JGfw==',
    'x-li-track': '{"clientVersion":"1.10.6369","mpVersion":"1.10.6369","osName":"web","timezoneOffset":5,"timezone":"Asia/Karachi","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
    'x-restli-protocol-version': '2.0.0',
}

linksfile = open('linkedinprofileurl.txt', 'r')
links = linksfile.read().split('\n')

headers_csv = ["LinkedIn URL","Name","# of follower","About","LinkedIn Premium",
               "Job #","Role","Company","Description","Start Month",
               "Start Year","End Month","End Year","Location"]
filecsv = open('linkdinexperiance.csv','w',encoding='utf-8',newline='')
writer = csv.DictWriter(filecsv,fieldnames=headers_csv)
writer.writeheader()
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.linkedin.com/login')
    time.sleep(1)
    driver.find_element_by_id('username').send_keys('rixtysoft01@gmail.com')
    time.sleep(1)
    driver.find_element_by_id('password').send_keys('qwerty123uiop')
    time.sleep(1)
    driver.find_element_by_css_selector('button[aria-label="Sign in"]').click()
    time.sleep(1)
    for link in links:
        driver.get(link)
        time.sleep(5)
        ps = driver.page_source
        res = scrapy.Selector(text=ps)
        name = res.css('h1::text').extract_first()
        followers = res.css('div.pvs-header__container > div > div > div > p > span:nth-child(1)::text').extract_first()
        about = ''.join(res.css('div.display-flex.ph5.pv3 > div > div > div ::text').extract()).strip()
        try:
            res.css('.pv-member-badge.pv-member-badge--for-top-card.inline-flex.p3')
            linkedinpremium = 'yes'
        except:
            linkedinpremium = 'no'
        try:
            experiancelink = [v for v in res.css('.artdeco-card.ember-view.relative.break-words.pb3.mt2 a::attr(href)').extract() if 'experience' in v][0]
            driver.get(experiancelink)
            time.sleep(5)
            ps = driver.page_source
            response = scrapy.Selector(text=ps)

            experiances = response.css('div.pvs-list__container > div > div.scaffold-finite-scroll__content > ul > li')
            for i,ex in enumerate(experiances):
                item = dict()
                item['Job #'] = i+1
                item['Role'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div span span::text').extract_first('').strip()
                item['Company'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(2) span::text').extract_first('').split('·')[0].strip()
                item['Description'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container span::text').extract_first('').strip()
                item['Start Month'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[0].strip().split()[0]
                item['Start Year'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[0].strip().split()[1]
                try:
                    item['End Month'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[1].strip().split()[0]
                except:
                    item['End Month'] = 'Present'
                if '·' not in ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[1].strip().split()[1]:
                    item['End Year'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[1].strip().split()[1]
                else:
                    item['End Year'] = 'Present'
                item['Location'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(4) span::text').extract_first('').strip()
                item['Name'] = name
                item['# of follower'] = followers
                item['About'] = about
                item['LinkedIn Premium'] = linkedinpremium
                item['LinkedIn URL'] = link
                writer.writerow(item)
                filecsv.flush()
        except:
            experiances = res.css('section:nth-child(4) div.pvs-list__outer-container > ul > li')
            for i,ex in enumerate(experiances):
                item = dict()
                item['Job #'] = i + 1
                item['Role'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > div span span::text').extract_first('').strip()
                item['Company'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(2) span::text').extract_first('').split('·')[0].strip()
                item['Description'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.pvs-list__outer-container span::text').extract_first('').strip()
                item['Start Month'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[0].strip().split()[0]
                item['Start Year'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[0].strip().split()[1]
                try:
                    item['End Month'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[1].strip().split()[0]
                except:
                    item['End Month'] = 'Present'
                try:
                    item['End Year'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(3) span::text').extract_first('').split('-')[1].strip().split()[1]
                except:
                    item['End Year'] = 'Present'
                item['Location'] = ex.css('div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > div.display-flex.flex-column.full-width > span:nth-child(4) span::text').extract_first('').strip()
                item['Name'] = name
                item['# of follower'] = followers
                item['About'] = about
                item['LinkedIn Premium'] = linkedinpremium
                item['LinkedIn URL'] = link
                writer.writerow(item)
                filecsv.flush()

#     for link in links:
#         response = s.get(link)
#         time.sleep(10)
#         res = scrapy.Selector(text=response.text)
#         fsd_profile = [v for v in res.css('code ::text').extract() if 'fsd_profile' in v and '"data":{"entityUrn":' in v][0].split('fsd_profile:')[1].split('"],')[0]
#
#         s.headers = headers2
#         response = s.get(graphql)
#         time.sleep(10)
#         response_dict = response.json()
#         filejson = open(link.replace('/',' ')+'_.json','w')
#         json.dump(response_dict, filejson)