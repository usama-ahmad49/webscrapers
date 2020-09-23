import sys
import csv

import json
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options as ff_options


csv_file = "OLLI_bar_chart.csv"
csv_header = ['Expiration', 'Strike', 'Last', 'Theoretical', 'IV', 'Delta', 'Gamma', 'Rho', 'Theta', 'Vega', 'Volume',
              'Open Int', 'Vol/OI', 'Type', 'Last Trade', ]

file = open(csv_file, 'w', newline='')
writer = csv.DictWriter(file, fieldnames=csv_header)
writer.writeheader()


def get_dict_value(data, key_list, default=''):
    """

    gets a dictionary and key_list, apply key_list sequentially on dictionary and return value

    :param data: dictionary

    :param key_list: list of key

    :param default: return value if key not found

    :return:

    """

    for key in key_list:

        if data and isinstance(data, dict):

            data = data.get(key, default)

        else:

            return default

    return data

def getData(url,date):
    options = ff_options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    requests_data = [r for r in driver.requests if 'get?fields=symbo' in r.path]

    json_data = json.loads(requests_data[0].response.body)

    item = dict()
    data = get_dict_value(json_data, ['data'])
    for call in get_dict_value(data, ['Call']):
        item['Expiration'] = date
        item['Strike'] = call.get('strikePrice')
        item['Last'] = call.get('lastPrice')
        item['Theoretical'] = call.get('theoretical')
        item['IV'] = call.get('volatility')
        item['Delta'] = call.get('delta')
        item['Gamma'] = call.get('gamma')
        item['Rho'] = call.get('rho')
        item['Theta'] = call.get('theta')
        item['Vega'] = call.get('vega')
        item['Volume'] = call.get('volume')
        item['Open Int'] = call.get('openInterest')
        item['Vol/OI'] = call.get('volumeOpenInterestRatio')
        item['Type'] = call.get('optionType')
        item['Last Trade'] = call.get('tradeTime')
        writer.writerow(item)
        print('item entered')

    for put in get_dict_value(data, ['Put']):
        item['Expiration'] = date
        item['Strike'] = put.get('strikePrice')
        item['Last'] = put.get('lastPrice')
        item['Theoretical'] = put.get('theoretical')
        item['IV'] = put.get('volatility')
        item['Delta'] = put.get('delta')
        item['Gamma'] = put.get('gamma')
        item['Rho'] = put.get('rho')
        item['Theta'] = put.get('theta')
        item['Vega'] = put.get('vega')
        item['Volume'] = put.get('volume')
        item['Open Int'] = put.get('openInterest')
        item['Vol/OI'] = put.get('volumeOpenInterestRatio')
        item['Type'] = put.get('optionType')
        item['Last Trade'] = put.get('tradeTime')
        writer.writerow(item)
        print('item entered')

if __name__ == '__main__':
    # input_symbol=str(sys.argv)
    input_symbol='OLLI'

    url = 'https://www.barchart.com/stocks/quotes/{}/volatility-greeks'.format(input_symbol)
    options = ff_options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    requests_data = [r for r in driver.requests if 'get?fields=symbo' in r.path]

    json_data = json.loads(requests_data[0].response.body)

    exp_date = get_dict_value(json_data, ['meta', 'expirations'])
    month_date = exp_date.get('monthly')
    week_date = exp_date.get('weekly')
    for md in month_date:
        mon_url = 'https://www.barchart.com/stocks/quotes/{}/volatility-greeks?expiration={}&moneyness=allRows'.format(input_symbol,md + '-m')
        getData(mon_url,md)

    for wd in week_date:
        wek_url = 'https://www.barchart.com/stocks/quotes/{}/volatility-greeks?expiration={}&moneyness=allRows'.format(input_symbol,wd + '-w')
        getData(wek_url,wd)



