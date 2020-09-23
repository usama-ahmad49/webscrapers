import tweepy


CONSUMER_KEY = "2BzmDfeKSN5nk9HKckjLqsCy3"
CONSUMER_SECRET = "j5aYd2fGAAWPlPgeCbCfSLO4PDMInigZKVg3uH3nDV6mNIBpRZ"

ACCESS_TOKEN = "3728211501-Cdoyt2WiCEW9tgfzhHGG5ByiWlZQIaPB6tFvS6i"
ACCESS_TOKEN_SECRET = "FoKrfz34MDcq4cgopu4SoENhZU5FEh3iM7oYQ7XkPHQO9"

auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api=tweepy.API(auth)

# timeline = api.home_timeline()
# for tweet in timeline:
#     print(f"{tweet.user.name} said {tweet.text}")

#stat=api.get_status(1290922926116675584)
reply=api.reply_count(1290922926116675584)
print(reply)