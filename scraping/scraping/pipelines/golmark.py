from scraping.pipelines.base import BasePipeline
from scraping.models.golmark import Golmark, GlobalId


class GolmarkPipeline(BasePipeline):
    max_buffer_size = 1
    excluded_columns = ['created', 'modified']
    _class = Golmark

    def process_item(self, item, spider):
        post = Golmark.query.filter(Golmark.url == item['url']).first()
        data = self.create_data(item, Golmark, excluded_columns=self.excluded_columns)
        if post:
            data['globalId'] = post.globalId
            self.enqueue_add_with_ignore(data, _class=Golmark)
            post.session.commit()
        else:
            global_id = self.enqueue_item(GlobalId(**{'taken': 1})).id
            data['globalId'] = global_id
            self.enqueue_add_with_ignore(data, _class=Golmark)
        return item
