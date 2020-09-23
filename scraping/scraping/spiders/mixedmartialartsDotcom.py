import csv

import scrapy
from datetime import datetime

csv_columns = ['match_date', 'red_fighter_name', 'red_fighter_T_wins', 'red_fighter_T_loss',
               'red_fighter_T_draws', 'blue_fighter_name','blue_fighter_T_wins',
               'blue_fighter_T_loss', 'blue_fighter_T_draws', ]
csv_file = open('MMAdotcom.csv', 'w', encoding="utf-8", newline='')
writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
writer.writeheader()


class mixedmartialarts(scrapy.Spider):
    name = 'mixedmartialarts'
    title = 'MixedMartialArts'
    start_urls = ['https://www.mixedmartialarts.com/events/search?search=UFC']

    # def get_dict_value(data, key_list, default=''):
    #     """
    #     gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
    #     :param data: dictionary
    #     :param key_list: list of key
    #     :param default: return value if key not found
    #     :return:
    #     """
    #     for key in key_list:
    #         if data and isinstance(data, dict):
    #             data = data.get(key, default)
    #         else:
    #             return default
    #     return data

    def parse(self, response):
        events = response.css('#event-upcoming tbody tr')

        for event in events:
            date=event.css('td::text').extract_first()
            link=event.css('td a ::attr(href)').extract_first()
            if(link):
                yield scrapy.Request(link, callback=self.parse_events, meta={'match_date': date})

        # if (response.css('.pagination a::text').extract_first()[:5] == 'Older'):
        #     pagination = 'https://www.sherdog.com{}'.format(response.css('.pagination a::attr(href)').extract_first())
        #     yield scrapy.Request(pagination)

    def parse_events(self, response):
        item = dict()
        fights=response.css('#event-panel .fight-item')
        for fight in fights:
            item['match_date'] = response.meta['match_date']
            item['red_fighter_name'] = fight.css('.row .row.names .col-sm-4.col-xs-10.hidden-xs a::text').extract()[0]
            item['red_fighter_T_wins'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[0].split('-')[0]
            item['red_fighter_T_loss'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[0].split('-')[1]
            item['red_fighter_T_draws'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[0].split('-')[2]
            item['blue_fighter_name'] = fight.css('.row .row.names .col-sm-4.col-xs-10.hidden-xs a::text').extract()[1]
            item['blue_fighter_T_wins'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[1].split('-')[0]
            item['blue_fighter_T_loss'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[1].split('-')[1]
            item['blue_fighter_T_draws'] = fight.css('.row .row.stats .col-xs-4 ::text').extract()[1].split('-')[2]
            writer.writerow(item)
            print('row printed')
        yield item
