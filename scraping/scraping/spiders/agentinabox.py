import json

import requests
import scrapy
from selenium import webdriver

from AirtableApi import AirtableClient

basekey = 'appbGbfK06kKbzrUy'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PropertyDetails'

airtable_client = AirtableClient(apikey, basekey)

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '671',
    'content-type': 'application/json',
    'cookie': 'reauid=9c1d20170614000093fe3d60af000000b7830c00; Country=PK; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; _gid=GA1.3.1275777266.1614869778; s_vi=[CS]v1|30207A89724E6B51-40001D11450AAF1A[CE]; s_ecid=MCMID%7C91443557979951233383091044920615720620; s_cc=true; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18691%7CMCMID%7C91443557979951233383091044920615720620%7CMCAAMLH-1615561882%7C3%7CMCAAMB-1615561882%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1614964282s%7CNONE%7CMCAID%7C30207A89724E6B51-40001D11450AAF1A%7CvVersion%7C3.1.2; _sp_ses.2fe7=*; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fagency%2Fminus-the-agent-australia-KIVDKB~1614869779479%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Fagent-in-a-box-woombye-KRZTOT~1614869951670%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Fminus-the-agent-australia-KIVDKB~1614930351732%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Fagent-in-a-box-woombye-KRZTOT~1614957084490; _ga=GA1.3.1607217567.1614869778; _ga_F962Q8PWJ0=GS1.1.1614957082.3.1.1614957470.0; _sp_id.2fe7=a3882f6e-177f-4bf5-845f-869fc714c4ec.1614869778.3.1614957505.1614930347.6b0adffd-d875-4ce0-b07b-65bb6a7b813a; utag_main=v_id:0177fdbd49fd0008ee5a0a31f19903073004506b00bd0$_sn:3$_ss:0$_st:1614959304809$vapi_domain:realestate.com.au$dc_visit:3$ses_id:1614957081564%3Bexp-session$_pn:4%3Bexp-session$dc_event:9%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; s_sq=rea-live%3D%2526c.%2526a.%2526activitymap.%2526page%253Drea%25253Afind%252520agent%25253Aagency%252520page%2526link%253DShow%252520more%252520properties%2526region%253Dapp%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drea%25253Afind%252520agent%25253Aagency%252520page%2526pidt%253D1%2526oid%253Dfunctionun%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
    'dnt': '1',
    'origin': 'https://www.realestate.com.au',
    'referer': 'https://www.realestate.com.au/agency/agent-in-a-box-woombye-KRZTOT',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
}

prebody = {"operationName": "", "variables": {"input": {"agencyId": "KRZTOT", "page": 1, "pageSize": 12, "channel": "sold", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}


def parselinks(urllist, itemlist):
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
    processed = []
    url = 'https://www.realestate.com.au/find-agency/graphql'
    resp = requests.post(url, data=json.dumps(prebody), headers=headers)
    responsejson = json.loads(resp.content.decode('utf-8'))
    totalresults = responsejson['data']['agencyListings']['totalCount']
    pages = totalresults / 200
    if not pages.is_integer():
        pages = int(pages) + 1
    else:
        pages.__int__()
    i = 1
    while i <= pages:
        body = {"operationName": "", "variables": {"input": {"agencyId": "KRZTOT", "page": i, "pageSize": 200, "channel": "sold", "sort": "sold-date-desc"}}, "query": "query ($input: AgencyListingsRequest!) {\n  agencyListings(input: $input) {\n    totalCount\n    listings {\n      id\n      channel\n      address {\n        streetAddress\n        postcode\n        suburb\n        __typename\n      }\n      mainImage {\n        uri\n        server\n        __typename\n      }\n      displayPrice\n      displayDate\n      features {\n        bedrooms\n        bathrooms\n        parkingSpaces\n        __typename\n      }\n      url\n      __typename\n    }\n    next\n    __typename\n  }\n}\n"}
        i += 1
        resp = requests.post(url, data=json.dumps(body), headers=headers)
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
    parselinks(urllist, itemlist)
    driver.quit()
    airtable_client.insert_records(table_name, processed)
