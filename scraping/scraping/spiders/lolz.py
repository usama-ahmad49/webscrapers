try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session
import datetime
import time
from selenium import webdriver
import scrapy
from selenium.webdriver.firefox.options import Options as ff_Options
from typing import Any, Union

with open('config.json') as inputfile:
    data = json.load(inputfile)
string = "mysql://{}:{}@{}/{}?charset=utf8".format(data.get('username'), data.get('pasword'), data.get('host'),
                                                   data.get('database'))

engine_bbi = create_engine(string, encoding='utf-8', pool_size=20, pool_recycle=60)
db_session_bbi = scoped_session(session.sessionmaker(bind=engine_bbi, expire_on_commit=False))

engine_bbi.connect()


def read_file():
    datadict = dict()
    selectQuery = """SELECT * from lolz_data"""
    engine_bbi.connect()
    data = engine_bbi.execute(selectQuery)
    for row in data:
        datadict[row[0]] = {'date': row[1], 'website': row[2]}
    return datadict


def start_requests(link_url, file_dict_input):
    options = ff_Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options)
    driver.get(link_url)
    time.sleep(15)
    scroll_pause_time = 5
    last_height: Union[Union[int, str], Any] = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    response = scrapy.Selector(text=driver.page_source)
    links = response.css('a.marketIndexItem--Title ::attr(href)').extract()
    for link in links:
        link = 'https://lolz.guru/{}'.format(link)
        driver.get(link)
        resp_page = scrapy.Selector(text=driver.page_source)
        stream_id = resp_page.css('.marketItemView--counters a ::attr(href)').extract_first('').split('/')[
            -3] if len(
            resp_page.css('.marketItemView--counters a ::attr(href)').extract_first('').split('/')) >= 3 else ''

        if stream_id in file_dict_input.keys():
            if stream_id == '':
                continue
            file_dict_input[stream_id]['date'] = str(datetime.date.today())
            try:
                sqlInsertQuery = f"UPDATE lolz_data SET checked_date = '{file_dict_input[stream_id]['date']}' WHERE stream_id='{stream_id}';"
                engine_bbi.connect()
                engine_bbi.execute(sqlInsertQuery)

            except:
                print("Failed to insert record for streamId {}".format(stream_id))

        else:
            file_dict_input[stream_id] = {'date': datetime.date.today(), 'website': link}
            try:
                sqlInsertQuery = f"INSERT INTO lolz_data (stream_id, checked_date, website) VALUES ({stream_id},{file_dict_input[stream_id]['date']},{file_dict_input[stream_id]['website']})"
                engine_bbi.connect()
                engine_bbi.execute(sqlInsertQuery)

            except:
                print("Failed to insert record for streamId {}".format(stream_id))
    driver.quit()


if __name__ == '__main__':
    inputFile = open('inputvar.txt', 'r')
    for urlInput in inputFile.readlines():
        url = urlInput.replace('\n', '')
        file_dict = read_file()
        start_requests(url, file_dict)
