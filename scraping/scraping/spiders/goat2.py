import scrapy
import requests
import json
import cloudscraper

goat_sku = 'DH6927 111'
headers = {
    'authority': 'ac.cnstrc.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.goat.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

params = {
    'c': 'ciojs-client-2.27.10',
    'key': 'key_XT7bjdbvjgECO5d8',
    'i': '778c546d-41a5-4c0e-b56d-6a3d8de8a6aa',
    's': '4',
    'num_results_per_page': '25',
    '_dt': '1654779233399',
}

main_dic = dict()
main_dic['lowestResellPrice'] =dict()

main_dic['resellPrices']= dict()

main_dic['resellPrices']['goat']= dict()

search_json = json.loads(requests.get(f'https://ac.cnstrc.com/search/{goat_sku}', params=params, headers=headers).text)
search_id_goat = ''
slug = ''
for i in search_json['response']['results']:
    if i['data']['sku'] == goat_sku:
        search_id_goat = i['data']['id']
        slug = i['data']['slug']
        main_dic['lowestResellPrice']['goat'] = i['data']['lowest_price_cents']


headers2 = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.goat.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
data = '{"query":"","facetFilters":["product_template_id:'+search_id_goat+'"]}'
response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers, data=data).text)

try:

    for j in response_product:
        if ((j['shoeCondition'] == 'new_no_defects') and (j['stockStatus'] == 'multiple_in_stock')) or ((j['shoeCondition'] == 'new_no_defects') and (j['stockStatus'] == 'single_in_stock')):
            main_dic['resellPrices']['goat'][j['sizeOption']['value']] = j['lowestPriceCents']['amount'] / 100

except:
    print('there is an exception')


a=1