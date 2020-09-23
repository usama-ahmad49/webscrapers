from scraping.pipelines.base import BasePipeline
from scraping.models.twitter import Twitter


class TwitterPipeline(BasePipeline):
    max_buffer_size = 1
    excluded_columns = ['created', 'modified']
    _class = Twitter

    def process_item(self, item, spider):
        post = Twitter.query.filter(Twitter.tweetId == item['tweetId']).first()
        data = self.create_data(item, Twitter, excluded_columns=self.excluded_columns)
        if post:
            post.diggCount = item.get('diggCount')
            post.shareCount = item.get('shareCount')
            post.commentCount = item.get('commentCount')
            post.playCount = item.get('playCount')
            post.musicURL = item.get('musicURL')
            post.media = item['media']
            post.session.commit()
        else:
            self.enqueue_add_with_ignore(data, _class=Twitter)
        return item
