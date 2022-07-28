import scrapy
from scraping.spiders.YT_stats import YTstats
from scraping.spiders.youtubeReport import youtubeReport


class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        # API_KEY = 'AIzaSyB1uHIrJzQ5ePOJHvZi7OFS2DwNRGmCN-E'
        API_KEY = 'AIzaSyC5HexiQKeb2p5V55ai2Tem6irFNbiMCuw'
        channel_id = 'UCq-Fj5jknLsUf-MWSy4_brA'
        # channel_id = 'UChvh5649wD7lQjV4rvVKuJg'
        yt = YTstats(API_KEY, channel_id)
        yt.extract_all()
        yt.dump()  # dumps to .json
        ytreport=youtubeReport
        ytreport.parse(,
        for key, value in yt.video_data.items():
            item = dict()
            item['channelViews'] = yt.channel_statistics['viewCount']
            item['channelComments'] = yt.channel_statistics['commentCount']
            item['subscribers'] = yt.channel_statistics['subscriberCount']
            item['subscribersOnCreatedDate'] = yt.channel_statistics['subscriberCount']
            item['videos'] = yt.channel_statistics['videoCount']
            item['hiddenSubscribers'] = yt.channel_statistics['hiddenSubscriberCount'] if yt.channel_statistics['hiddenSubscriberCount'] else ''
            item['hiddenSubscribersOnCreatedDate'] = yt.channel_statistics['hiddenSubscriberCount'] if yt.channel_statistics['hiddenSubscriberCount'] else ''
            item['publishedAt'] = value['publishedAt']
            item['channelId'] = channel_id
            item['title'] = value['title']
            item['description'] = value['description']
            item['views'] = value['viewCount']
            item['likes'] = value['likeCount']
            item['disLike'] = value['dislikeCount']
            item['share'] = value['shares']
            item['estimatedMinutesWatched'] = value['estimatedMinutesWatched']
            # item['averageViewDuration'] = value['averageViewDuration']
            item['comments'] = value['commentCount']
            item['videoId'] = key
            item['thumbnail'] = value['thumbnails']['default']['url']
