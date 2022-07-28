import json
import time

import requests
import scrapy
from seleniumwire import webdriver

from AirtableApi import AirtableClient

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)


processed = []


# headers = {
# 'accept': '*/*',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'en-US,en;q=0.9',
# 'content-length': '646',
# 'content-type': 'application/json',
# 'cookie': 'reauid=9c1d20170614000093fe3d60af000000b7830c00; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; s_vi=[CS]v1|30207A89724E6B51-40001D11450AAF1A[CE]; s_ecid=MCMID%7C91443557979951233383091044920615720620; s_cc=true; mid=14319810835039164340; ab.storage.deviceId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%227ad533c2-be75-baa3-4e29-2515aeadd2bd%22%2C%22c%22%3A1614962437854%2C%22l%22%3A1614962437854%7D; Country=PK; AWSELB=BD21ABD912FD962534A86FF37C471AF8CEA612D2DA41CEB370542810C1BDB29FF6C64B003441577284C9C9332FB9815B2C31177FDAECEB148403CC82B090F5768236C21CB8; AWSELBCORS=BD21ABD912FD962534A86FF37C471AF8CEA612D2DA41CEB370542810C1BDB29FF6C64B003441577284C9C9332FB9815B2C31177FDAECEB148403CC82B090F5768236C21CB8; _stc=typedBookmarked; s_nr=1615212986593; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fagency%2Fminus-the-agent-australia-KIVDKB~1615286315671; ab.storage.sessionId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22cc7c4e82-afc5-1fcf-91dd-6de42130823e%22%2C%22e%22%3A1615288686011%2C%22c%22%3A1615286033584%2C%22l%22%3A1615286886011%7D; External=%2FRUBICON%3DKHYLOHZQ-1R-LISB%2FTRIPLELIFT%3D5062803671868968242%2F_EXP%3D1646498261%2F_exp%3D1646827298; _gid=GA1.3.1246347623.1615384246; _sp_ses.2fe7=*; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18697%7CMCMID%7C91443557979951233383091044920615720620%7CMCAAMLH-1616056113%7C3%7CMCAAMB-1616056113%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1615458513s%7CNONE%7CMCAID%7C30207A89724E6B51-40001D11450AAF1A%7CvVersion%7C3.1.2; utag_main=v_id:0177fdbd49fd0008ee5a0a31f19903073004506b00bd0$_sn:14$_ss:0$_st:1615454012965$vapi_domain:realestate.com.au$dc_visit:14$ses_id:1615451312574%3Bexp-session$_pn:2%3Bexp-session$dc_event:52%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _sp_id.2fe7=a3882f6e-177f-4bf5-845f-869fc714c4ec.1614869778.14.1615452214.1615384245.a8ebc5e5-3b65-4528-9f35-c56b492357b8; _ga=GA1.3.1607217567.1614869778; _ga_F962Q8PWJ0=GS1.1.1615451313.17.1.1615452452.0; s_sq=rea-live%3D%2526c.%2526a.%2526activitymap.%2526page%253Drea%25253Afind%252520agent%25253Aagency%252520page%2526link%253DShow%252520more%252520properties%2526region%253Dapp%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drea%25253Afind%252520agent%25253Aagency%252520page%2526pidt%253D1%2526oid%253Dfunctionun%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
# 'dnt': '1',
# 'origin': 'https://www.realestate.com.au',
# 'referer': 'https://www.realestate.com.au/agency/minus-the-agent-australia-KIVDKB',
# 'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-fetch-dest': 'empty',
# 'sec-fetch-mode': 'cors',
# 'sec-fetch-site': 'same-origin',
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
# }
prebodysold = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": 1, "pageSize": 12, "channel": "sold", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
prebodybuy = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": 1, "pageSize": 12, "channel": "buy", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
prebodyrent = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": 1, "pageSize": 12, "channel": "rent", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}


def parse(urllist, itemlist):
    for i, link in enumerate(urllist):
        driver.get(link)
        ps = driver.page_source
        da = scrapy.Selector(text=ps)
        newitem = itemlist[i]
        newitem['TotalArea'] = ''.join(da.css('.property-size.rui-clearfix ::text').extract()).strip()
        try:
            newitem['Contact'] = da.css('.phone a::attr(href)').extract_first().split(':')[-1]
        except:
            pass
        try:
            newitem['State'] = da.css('.property-info-address ::text').extract_first().split(',')[-1].split()[0]
        except:
            pass
        newitem['Description'] = ' '.join(da.css('.property-description__content ::text').extract())
        processed.append(newitem)


if __name__ == '__main__':
    urllist = []
    itemlist = []
    url = 'https://www.realestate.com.au/agency/minus-the-agent-australia-KIVDKB'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_css_selector('#app > section > div.Styles__AgencyProfileSection-sc-1s0692j-0.eANdJm > div > div > div > div:nth-child(1) > div > div.sc-dxgOiQ.fcVasU > button').click()
    time.sleep(2)
    headers = [v for v in driver.requests if 'https://www.realestate.com.au/find-agency/graphql' in v.url][0].headers
    time.sleep(1)
    driver.quit()
    newurl = "https://www.realestate.com.au/find-agency/graphql"
    # sold
    respsold = requests.post(newurl, data=json.dumps(prebodysold), headers=headers)
    responsejson = json.loads(respsold.content.decode('utf-8'))
    totalresultssold = responsejson['data']['agencyListings']['totalCount']
    pagesold = totalresultssold / 200
    if not pagesold.is_integer():
        pagesold = int(pagesold) + 1
    else:
        pagesold.__int__()
    i = 1
    while i <= pagesold:
        bodysold = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": i, "pageSize": 200, "channel": "sold", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
        i += 1
        resp = requests.post(newurl, data=json.dumps(bodysold), headers=headers)
        responsejson = json.loads(resp.content.decode('utf-8'))
        for res in responsejson['data']['agencyListings']['listings']:
            item = dict()
            item['url'] = res['url']
            item['Domain'] = 'agentinabox.com.au'
            item['Listing Type'] = res['channel']
            item['Title'] = res['address']['streetAddress']
            item['Street'] = res['address']['streetAddress']
            item['Suburb'] = res['address']['suburb']
            item['ZipCode'] = res['address']['postcode']
            item['Price'] = res['displayPrice']
            item['Property ID'] = res['id']
            item['Bedrooms'] = str(res['features']['bedrooms'])
            item['Bathrooms'] = str(res['features']['bathrooms'])
            item['ParkingSpaces'] = str(res['features']['parkingSpaces'])
            item['Main Image'] = [{"url": res['mainImage']['server'] + res['mainImage']['uri']}]
            urllist.append(res['url'])
            itemlist.append(item)
    # buy
    respbuy = requests.post(newurl, data=json.dumps(prebodybuy), headers=headers)
    responsejson = json.loads(respbuy.content.decode('utf-8'))
    totalresultsbuy = responsejson['data']['agencyListings']['totalCount']
    pagebuy = totalresultsbuy / 200
    if not pagebuy.is_integer():
        pagebuy = int(pagebuy) + 1
    else:
        pagebuy.__int__()
    i = 1
    while i <= pagebuy:
        bodybuy = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": i, "pageSize": 200, "channel": "buy", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
        i += 1
        resp = requests.post(newurl, data=json.dumps(bodybuy), headers=headers)
        responsejson = json.loads(resp.content.decode('utf-8'))
        for res in responsejson['data']['agencyListings']['listings']:
            item = dict()
            item['url'] = res['url']
            item['Domain'] = 'agentinabox.com.au'
            item['Listing Type'] = res['channel']
            item['Title'] = res['address']['streetAddress']
            item['Street'] = res['address']['streetAddress']
            item['Suburb'] = res['address']['suburb']
            item['ZipCode'] = res['address']['postcode']
            item['Price'] = res['displayPrice']
            item['Property ID'] = res['id']
            try:
                item['Bedrooms'] = str(res['features']['bedrooms'])
            except:
                pass
            try:
                item['Bathrooms'] = str(res['features']['bathrooms'])
            except:
                pass
            try:
                item['ParkingSpaces'] = str(res['features']['parkingSpaces'])
            except:
                pass
            item['Main Image'] = [{"url": res['mainImage']['server'] + res['mainImage']['uri']}]
            urllist.append(res['url'])
            itemlist.append(item)
    # rent
    respbuy = requests.post(newurl, data=json.dumps(prebodyrent), headers=headers)
    responsejson = json.loads(respbuy.content.decode('utf-8'))
    totalresultsrent = responsejson['data']['agencyListings']['totalCount']
    pagerent = totalresultsrent / 200
    if not pagerent.is_integer():
        pagerent = int(pagerent) + 1
    else:
        pagerent.__int__()
    i = 1
    while i <= pagerent:
        bodyrent = {"operationName": "", "variables": {"input": {"agencyId": "KIVDKB", "page": i, "pageSize": 200, "channel": "rent", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
        i += 1
        resp = requests.post(newurl, data=json.dumps(bodyrent), headers=headers)
        responsejson = json.loads(resp.content.decode('utf-8'))
        for res in responsejson['data']['agencyListings']['listings']:
            item = dict()
            item['url'] = res['url']
            item['Domain'] = 'agentinabox.com.au'
            item['Listing Type'] = res['channel']
            item['Title'] = res['address']['streetAddress']
            item['Street'] = res['address']['streetAddress']
            item['Suburb'] = res['address']['suburb']
            item['ZipCode'] = res['address']['postcode']
            item['Price'] = res['displayPrice']
            item['Property ID'] = res['id']
            item['Bedrooms'] = str(res['features']['bedrooms'])
            item['Bathrooms'] = str(res['features']['bathrooms'])
            item['ParkingSpaces'] = str(res['features']['parkingSpaces'])
            item['Main Image'] = [{"url": res['mainImage']['server'] + res['mainImage']['uri']}]
            urllist.append(res['url'])
            itemlist.append(item)

    driver = webdriver.Ie()
    parse(urllist, itemlist)
    driver.quit()
    airtable_client.insert_records(table_name, processed)
