try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import datetime
import json

import tweepy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session

# set wait_on_rate_limit =True; as twitter may block you from querying if it finds you exceeding some limits

inputfile = open('config.json')
data = json.load(inputfile)
string = "mysql://{}:{}@{}/{}?charset=utf8".format(data.get('username'), data.get('password'), data.get('host'),
                                                   data.get('database'))
auth = tweepy.OAuthHandler(data.get('CONSUMER_KEY'), data.get('CONSUMER_SECRET'))
auth.set_access_token(data.get('ACCESS_TOKEN'), data.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth,wait_on_rate_limit=True)

engine_bbi = create_engine(string, encoding='utf-8', pool_size=20, pool_recycle=60)
db_session_bbi = scoped_session(session.sessionmaker(bind=engine_bbi, expire_on_commit=False))

engine_bbi.connect()


def read_file():
    datadict = dict()
    selectQuery = """SELECT * from indexed_players"""
    engine_bbi.connect()
    data = engine_bbi.execute(selectQuery)
    for row in data:
        datadict[row[0]] = {'date': row[1], 'website': row[2]}
    return datadict


if __name__ == '__main__':
    file_dict_input = read_file()
    new_tweets = api.user_timeline(screen_name='rusthackreport', count=200)
    getting_data = True
    counts_done = 0
    while getting_data:
        if new_tweets.__len__()==0:
            break
        for tweet in new_tweets:
            counts_done += 1
            # print('scraped tweets count: {}'.format(counts_done))
            try:
                link = tweet.entities['urls'][0]['expanded_url']

            except:
                continue
            steam_id = link.split('/')[-1]
            if steam_id in file_dict_input.keys():
                if steam_id == '':
                    continue
                file_dict_input[steam_id]['date'] = datetime.datetime.now()
                try:
                    sqlInsertQuery = f"UPDATE indexed_players SET checked_date = CAST('{str(file_dict_input[steam_id]['date'])}' AS datetime) WHERE steam_id='{steam_id}';"
                    engine_bbi.connect()
                    engine_bbi.execute(sqlInsertQuery)

                except Exception as e:
                    print("Failed to update record for steamId {}".format(steam_id))

            else:
                if steam_id.strip() == '':
                    continue
                file_dict_input[steam_id] = {'date': str(datetime.datetime.now()), 'website': 'https://twitter.com/'}
                try:
                    sqlInsertQuery = f"INSERT IGNORE INTO indexed_players (steam_id, checked_date, website) VALUES ('{steam_id}', CAST('{str(file_dict_input[steam_id]['date'])}' AS datetime),'{file_dict_input[steam_id]['website']}')"
                    engine_bbi.connect()
                    engine_bbi.execute(sqlInsertQuery)

                except Exception as e:
                    print("Failed to insert record for steamId {}".format(steam_id))
        oldest = new_tweets[-1].id - 1
        new_tweets = api.user_timeline(screen_name='rusthackreport', count=200, max_id=oldest)
        print('scraped tweets count: {}'.format(counts_done))
    print('Program ends! No more tweets')
