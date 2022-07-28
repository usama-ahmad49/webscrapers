import csv
import logging
import requests
import csvdiff
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_token():
  url = "https://admin.brandrange.com/index.php/rest/V1/integration/admin/token"

  # headers = CaseInsensitiveDict()
  headers = dict()
  headers["Content-Type"] = "application/json"

  data = '{"username":"nauman.pucit", "password":"nauman.pucit@160#"}'

  resp = requests.post(url, headers=headers, data=data)
  token = resp.text.replace('"', '')
  return token

if __name__ == '__main__':
    headers = ['sku', 'name']
    fileopen = open('duplicate_sku.csv','w',newline='', encoding='utf-8')
    writerduplicate = csv.DictWriter(fileopen,fieldnames=headers)
    writerduplicate.writeheader()
    existing_skus = []
    magento_token = get_token()
    logger.info(f'CloseUp called')
    logger.info(f'Getting data from Magento')
    headersMagento = {'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {magento_token}'}
    originalproducts = []
    duplicateProducts = []
    #for men
    TRS = requests.get(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=attribute_set_id&searchCriteria[filterGroups][0][filters][0][value]=27&&searchCriteria[filterGroups][1][filters][1][field]=type_id&searchCriteria[filterGroups][1][filters][1][value]=configurable&searchCriteria[pageSize]=1&store_id=1,store_code=en', headers=headersMagento)
    TotalresultsJson = json.loads(TRS.content.decode('utf-8'))
    TotalCount = TotalresultsJson['total_count']
    page = TotalCount / 1000
    if page.is_integer():
        TotalPages = page
    else:
        TotalPages = int(page) + 1
    i = 1
    logger.info(f'TotalPage = {TotalPages}')
    while i <= TotalPages:
        logger.info(f'Getting data from Magento ## page = {i}')
        resp = requests.get(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=attribute_set_id&searchCriteria[filterGroups][0][filters][0][value]=27&&searchCriteria[filterGroups][1][filters][1][field]=type_id&searchCriteria[filterGroups][1][filters][1][value]=configurable&searchCriteria[pageSize]=1000&searchCriteria[currentPage]={i}&store_id=1,store_code=en', headers=headersMagento)
        jdata = json.loads(resp.content.decode('utf-8'))
        for data in jdata['items']:
            if data['type_id'] == 'configurable':
                if data['status'] == 1:
                    if data['name'] in originalproducts:
                        item = dict()
                        duplicateProducts.append(data['name'])
                        item['sku'] = data['sku']
                        item['name'] = data['name']
                        writerduplicate.writerow(item)
                    else:
                        originalproducts.append(data['name'])
            # if data['sku'].split('-')[-1].replace('.','1').isdigit() or data['sku'].split('-')[-1] == 'OS':

        i += 1
    # for women
    TRS = requests.get(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=attribute_set_id&searchCriteria[filterGroups][0][filters][0][value]=26&&searchCriteria[filterGroups][1][filters][1][field]=type_id&searchCriteria[filterGroups][1][filters][1][value]=configurable&searchCriteria[pageSize]=1&store_id=1,store_code=en', headers=headersMagento)
    TotalresultsJson = json.loads(TRS.content.decode('utf-8'))
    TotalCount = TotalresultsJson['total_count']
    page = TotalCount / 1000
    if page.is_integer():
        TotalPages = page
    else:
        TotalPages = int(page) + 1
    i = 1
    logger.info(f'TotalPage = {TotalPages}')
    while i <= TotalPages:
        logger.info(f'Getting data from Magento ## page = {i}')
        resp = requests.get(f'https://admin.brandrange.com/index.php/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=attribute_set_id&searchCriteria[filterGroups][0][filters][0][value]=26&&searchCriteria[filterGroups][1][filters][1][field]=type_id&searchCriteria[filterGroups][1][filters][1][value]=configurable&searchCriteria[pageSize]=1000&searchCriteria[currentPage]={i}&store_id=1,store_code=en', headers=headersMagento)
        jdata = json.loads(resp.content.decode('utf-8'))
        for data in jdata['items']:
            if data['type_id'] == 'configurable':
                if data['status'] == 1:
                    if data['name'] in originalproducts:
                        item = dict()
                        duplicateProducts.append(data['name'])
                        item['sku'] = data['sku']
                        item['name'] = data['name']
                        writerduplicate.writerow(item)
                    else:
                        originalproducts.append(data['name'])

        i += 1