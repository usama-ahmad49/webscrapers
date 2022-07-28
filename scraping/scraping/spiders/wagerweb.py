import json
import time
from copy import deepcopy
import datetime
from datetime import timedelta

import requests
import scrapy
import unidecode
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

game = []
dontscrape = ['Aussie Rules', 'Futsal', 'Golf', 'Handball', 'Rugby League', 'Rugby Union', 'Snooker', 'Upcoming Games', 'Volleyball', 'Table Tennis']

fileout = open('waggerweb.json', 'w', encoding='utf-8')
totalresluts = []

ini_time_for_now = datetime.datetime.now()
future_date_after_1day = ini_time_for_now + \
                         timedelta(days=1)
class wagerweb(scrapy.Spider):
    name = 'wagerweb'

    def start_requests(self):
        # options = Options()
        # options.add_argument('--headless')
        url = "https://be.wagerweb.eu/"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="customerIDid"]').send_keys('484495')
        driver.find_element_by_xpath('//*[@id="LoginForm"]/input[2]').send_keys('DPlatt077!')
        driver.find_element_by_xpath('//*[@id="Login"]').click()
        time.sleep(30)
        headers = [v for v in driver.requests if 'https://web02.wagerweb.eu/web/v1/bets/betsTreeMenu' in v.url][0].headers
        driver.quit()
        req = requests.get(url='https://web02.wagerweb.eu/web/v1/bets/betsTreeMenu', headers=headers)
        res = json.loads(req.text)
        for re in res['tree'][1:]:
            for name in re['children']:
                if name['sport'] in dontscrape:
                    continue
                if 'Futures' in name['subSport']:
                    continue
                game.append(name['sport'] + ',' + name['subSport'])
        for ga in game:
            url = f"https://web02.wagerweb.eu/web/v2/search/eventsBySportSubSport?periodNumber=-1&sport={ga.split(',')[0]}&subSport={ga.split(',')[1]}"
            yield scrapy.Request(url=url, headers=dict(headers))

    def parse(self, response, **kwargs):
        resjson = json.loads(response.text)
        for event in resjson['Events']:
            if event['markets'].__len__() == 0:
                continue
            if str(future_date_after_1day)>event['startTime'].replace('T',' ').replace('Z',''):
                perioddict = dict()
                game = dict()
                for markets in event['markets']:
                    if markets['periodName'] == 'Game':
                        game['sportsbook_name'] = "wagerweb"
                        game['Game Title'] = event['sport']
                        game['league'] = event['league']
                        game['Date'] = event['startTime'].split('T')[0]
                        try:
                            game['Time'] = event['startTime'].split('T')[1].split('.')[0]
                        except:
                            game['Time'] = event['startTime'].split('T')[1]
                        game['FirstTeam'] = event['participants'][0]['name']
                        game['SecondTeam'] = event['participants'][1]['name']
                        for checkdraw in markets['outcomes']:
                            if checkdraw['outcome'] == 'draw':
                                game['Draw'] = str(checkdraw['points']) + ' , ' + str(checkdraw['price'])
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['constant_data'] = deepcopy(game)

                    if markets['periodName'] == '1st Half':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        for checkdraw in markets['outcomes']:
                            if checkdraw['outcome'] == 'draw':
                                game['Draw'] = str(checkdraw['points']) + ' , ' + str(checkdraw['price'])
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['1st Half'] = game

                    if markets['periodName'] == '2nd Half':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        for checkdraw in markets['outcomes']:
                            if checkdraw['outcome'] == 'draw':
                                game['Draw'] = str(checkdraw['points']) + ' , ' + str(checkdraw['price'])
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['2nd Half'] = game

                    if markets['periodName'] == '1st Quater':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['1st Quater'] = game

                    if markets['periodName'] == '2nd Quater':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['2nd Quater'] = game

                    if markets['periodName'] == '3rd Quater':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['3rd Quater'] = game

                    if markets['periodName'] == '4th Quater':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['4th Quater'] = game

                    if markets['periodName'] == '1st 5 Innings':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        for checkdraw in markets['outcomes']:
                            if checkdraw['outcome'] == 'draw':
                                game['Draw'] = str(checkdraw['points']) + ' , ' + str(checkdraw['price'])
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['1st 5 Innings'] = game

                    if markets['periodName'] == '3 Way Line':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['3 Way Line'] = game

                    if markets['periodName'] == '3 Way Line':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['3 Way Line'] = game

                    if markets['periodName'] == '1st Period':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['1st Period'] = game

                    if markets['periodName'] == '2nd Period':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['2nd Period'] = game

                    if markets['periodName'] == '3rd Period':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['3rd Period'] = game

                    if markets['periodName'] == 'Regulation':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['Regulation'] = game

                    if markets['periodName'] == '1st Set':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['1st Set'] = game

                    if markets['periodName'] == '2nd Set':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['2nd Set'] = game

                    if markets['periodName'] == '3rd Set':
                        try:
                            del game['sportsbook_name']
                        except:
                            pass
                        try:
                            del game['Game Title']
                        except:
                            pass
                        try:
                            del game['league']
                        except:
                            pass
                        try:
                            del game['Date']
                        except:
                            pass
                        try:
                            del game['Time']
                        except:
                            pass
                        try:
                            del game['FirstTeam']
                        except:
                            pass
                        try:
                            del game['SecondTeam']
                        except:
                            pass
                        if markets['marketType'] == 'Spread':
                            game['Team1spread'] = str(markets['outcomes'][0]['points']) + ' , ' + str(markets['outcomes'][0]['price'])
                            game['Team2spread'] = str(markets['outcomes'][1]['points']) + ' , ' + str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Moneyline':
                            game['Team1money'] = str(markets['outcomes'][0]['price'])
                            game['Team2money'] = str(markets['outcomes'][1]['price'])
                        if markets['marketType'] == 'Total':
                            for total in markets['outcomes']:
                                if total['outcome'] == 'over':
                                    game['total_over'] = str(total['points']) + ' , ' + str(total['price'])
                                if total['outcome'] == 'under':
                                    game['total_under'] = str(total['points']) + ' , ' + str(total['price'])
                        perioddict['3rd Set'] = game
                totalresluts.append(perioddict)

    def close(spider, reason):
        items_json_str = json.dumps(totalresluts, indent=4)
        items_json_str = unidecode.unidecode(items_json_str)
        fileout.write(items_json_str)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(wagerweb)
process.start()
