import json

import requests

if __name__ == '__main__':
    productskulist = []
    file = open('stockx_skus.txt', 'w', encoding='utf-8')
    url = "https://admin.brandrange.com/index.php/rest/V1/integration/admin/token"

    # headers = CaseInsensitiveDict()
    headers  = dict()
    headers["Content-Type"] = "application/json"

    data = '{"username":"nauman.pucit", "password":"nauman.pucit@160#"}'

    resp = requests.post(url, headers=headers, data=data)
    token = resp.text.replace('"','')
    #
    # print(resp.status_code)
    headersMagento = {'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    TRS = requests.get('https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=IRC&searchCriteria[filterGroups][0][filters][0][value]=SNEAKERS STOCK | DS&searchCriteria[pageSize]=1&store_id=1,store_code=en', headers=headersMagento)
    TotalresultsJson = json.loads(TRS.content.decode('utf-8'))
    TotalCount = TotalresultsJson['total_count']
    count = 0
    page = TotalCount / 1000
    if page.is_integer():
        TotalPages = page
    else:
        TotalPages = int(page) + 1
    i = 1
    while i <= TotalPages:
        resp = requests.get(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=IRC&searchCriteria[filterGroups][0][filters][0][value]=SNEAKERS STOCK | DS&searchCriteria[pageSize]=1000&searchCriteria[currentPage]={i}&store_id=1,store_code=en&fields=items[sku]', headers=headersMagento)
        jdata = json.loads(resp.content.decode('utf-8'))
        for data in jdata['items']:
            if data['sku'].split('-')[-1].replace('.','1').isdigit() or data['sku'].split('-')[-1] == 'OS':
                if '-'.join(data['sku'].split('-')[:-2]) not in productskulist:
                    productskulist.append('-'.join(data['sku'].split('-')[:-2]))
            elif data['sku'].split('-').__len__() ==2:
                if data['sku'].split('-')[:-1] not in productskulist:
                    productskulist.append('-'.join(data['sku'].split('-')[:-1]))
        file.flush()
        i+=1
    for sku in productskulist:
        file.write(sku + '\n')
    file.close()