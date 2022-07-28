import json
import csv
import requests
from operator import itemgetter

csvheader = ['Company Name', 'Company Symbol', 'Company Last', 'Company Probability']
fileout = open('stockpicker.csv','w', newline='',encoding='utf-8')
writer = csv.DictWriter(fileout,fieldnames=csvheader)
writer.writeheader()
headers = {"accept": "text/plain, */*; q=0.01",
           "accept-language": "en-US,en;q=0.9",
           "content-length": "509",
           "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
           "cookie": "_ga=GA1.2.89974416.1614586726; _gid=GA1.2.1238737436.1614586726; _sp_ses.cf1a=*; _sp_id.cf1a=98d56cd8-ddd7-4d14-be3d-f5ec7afc1952.1614586725.2.1614590307.1614586725.dbc32e4f-5206-4b6a-b628-482517fabde7",
           "dnt": "1",
           "origin": "https://www.tradingview.com",
           "referer": "https://www.tradingview.com/",
           "sec-fetch-dest": "empty",
           "sec-fetch-mode": "cors",
           "sec-fetch-site": "same-site",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
           }

formdata1st = {
    "filter": [{"left": "name", "operation": "nempty"}],
    "options": {"lang": "en"},
    "symbols": {"query": {"types": []}, "tickers": [], "groups": [{"type": "index", "values": ["SP:SPX"]}]},
    "columns": ["logoid", "name", "close", "change", "change_abs", "Recommend.All", "volume", "market_cap_basic", "price_earnings_ttm", "earnings_per_share_basic_ttm", "number_of_employees", "sector", "description", "name", "type", "subtype", "update_mode", "pricescale", "minmov", "fractional", "minmove2"],
    "sort": {"sortBy": "name", "sortOrder": "asc"},
    "range": [0, 10]
}

if __name__ == '__main__':
    total = 0.0
    listofitems = []
    respcount = requests.post(url='https://scanner.tradingview.com/america/scan', headers=headers, json=formdata1st)
    jsondatacount = json.loads(respcount.content.decode('utf-8'))
    range = jsondatacount.get('totalCount')
    formdata = {
        "filter": [{"left": "name", "operation": "nempty"}],
        "options": {"lang": "en"},
        "symbols": {"query": {"types": []}, "tickers": [], "groups": [{"type": "index", "values": ["SP:SPX"]}]},
        "columns": ["logoid", "name", "close", "change", "change_abs", "Recommend.All", "volume", "market_cap_basic", "price_earnings_ttm", "earnings_per_share_basic_ttm", "number_of_employees", "sector", "description", "name", "type", "subtype", "update_mode", "pricescale", "minmov", "fractional", "minmove2"],
        "sort": {"sortBy": "name", "sortOrder": "asc"},
        "range": [0, int(f'{range}')]
    }
    resp = requests.post(url='https://scanner.tradingview.com/america/scan', headers=headers, json=formdata)
    jsondata = json.loads(resp.content.decode('utf-8'))
    for data in jsondata['data']:
        total += data['d'][2]
    for da in jsondata['data']:
        item = dict()
        item['Company Name'] = da['d'][0]
        item['Company Symbol'] = da['d'][1]
        item['Company Last'] = da['d'][2]
        item['Company Probability'] = da['d'][2] / total
        listofitems.append(item)
    listofitems=sorted(listofitems, key=itemgetter('Company Probability'), reverse=False)  #if sorting in decending order set reverse = True
    for item in listofitems:
        writer.writerow(item)
        fileout.flush()
