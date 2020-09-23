import json
import time

from scraping.spiders.base_spider import BaseSpider

import tweepy
from tweepy import API
from tweepy import OAuthHandler
import requests
import scrapy

ACCESS_TOKEN = "3728211501-Cdoyt2WiCEW9tgfzhHGG5ByiWlZQIaPB6tFvS6i"
ACCESS_TOKEN_SECRET = "FoKrfz34MDcq4cgopu4SoENhZU5FEh3iM7oYQ7XkPHQO9"
CONSUMER_KEY = "2BzmDfeKSN5nk9HKckjLqsCy3"
CONSUMER_SECRET = "j5aYd2fGAAWPlPgeCbCfSLO4PDMInigZKVg3uH3nDV6mNIBpRZ"


class TwitterSpider(BaseSpider):
    name = 'twitter'
    title = 'Twitter'
    start_urls = ['http://quotes.toscrape.com/page/1/']
    google_sheet_url = ('https://docs.google.com/spreadsheets/d/1npltM5YITcyxvGc3_NEbZA7Hj5z711-ARAIafSD-lzM/export?'
                        'format=csv&id=1npltM5YITcyxvGc3_NEbZA7Hj5z711-ARAIafSD-lzM&gid=0')
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {'scraping.pipelines.twitter.TwitterPipeline': 600}
    }
    companies = []

    def open_spider(self, spider):
        response = requests.get(self.google_sheet_url)
        self.companies = response.content.decode('utf-8').split()

    def parse(self, response):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        auth_api = API(auth)
        tweepy.Cursor(auth_api.search, q="#hashtag", count=5, include_entities=True)
        users = self.companies
        for user in users:
            # user = 'naumanShareef1'
            item = dict()
            all_tweets = []
            user_item = auth_api.get_user(user)
            new_tweets = auth_api.user_timeline(screen_name=user, count=200)
            user_item = user_item.__dict__
            item['followersCount'] = user_item.get('followers_count')
            item['followersCountOnCreatedDate'] = user_item.get('followers_count')
            item['userId'] = user_item['id']
            # saved_tweets = t_model.query.filter(t_model.userId == item['userId'])
            # for s_tweet in saved_tweets:
            #     s_tweet.followersCount = user_item.get('followers_count')
            # saved_tweets.session.commit()
            item['userName'] = user_item.get('name')
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            while len(new_tweets) > 0:
                print(f"getting tweets before {oldest}")
                new_tweets = auth_api.user_timeline(screen_name=user, count=200, max_id=oldest)
                all_tweets.extend(new_tweets)
                oldest = all_tweets[-1].id - 1
                print(f"...{len(all_tweets)} tweets downloaded so far")
                time.sleep(5)
                for tweet in new_tweets:
                    tweet = tweet.__dict__
                    tweet_item = dict()
                    tweet_item.update(item)
                    tweet_item['tweetId'] = tweet.get('id_str')
                    tweet_item['text'] = tweet.get('text', '')[:49]
                    tweet_item['tweetCreatedDate'] = tweet.get('created_at')
                    tweet_item['retweetCount'] = tweet.get('retweet_count')
                    tweet_item['favoriteCount'] = tweet.get('favorite_count')
                    tweet_single = auth_api.get_status(tweet_item['tweetId'], tweet_mode="extended")
                    if hasattr(tweet_single, 'entities') and 'media' in tweet_single.entities:
                        media_data = []
                        for media in tweet_single.entities['media']:
                            media_data.append({'url': media['url'], 'type': media['type']})
                        tweet_item['media'] = json.dumps(media_data)
                        # yield tweet_item
                        yield scrapy.Request('https://twitter.com/{}/status/{}'.format(user, tweet['id']),
                                             meta={'tweet': tweet_item}, callback=self.get_replies)

    def get_replies(self, response):
        tweet_item = response.meta['tweet']
        replies_count = response.css(
            '#profile-tweet-action-reply-count-aria-{} ::text'.format(tweet_item['tweetId'])).extract_first('').replace(
            'replies', '').strip()
        tweet_item['replies'] = int(replies_count) if replies_count.isnumeric() else 0
        tweet_item['engagement'] = tweet_item['favoriteCount'] + tweet_item['retweetCount'] + tweet_item[
            'replies']
        tweet_item['engagementRate'] = (tweet_item['favoriteCount'] + tweet_item['retweetCount'] +
                                        tweet_item[
                                            'replies']) / tweet_item['followersCountOnCreatedDate']
        yield tweet_item

