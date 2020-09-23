import csv

import scrapy
from datetime import datetime

csv_columns=['match_date','red_fighter_name','red_fighter_result','red_fighter_T_wins','red_fighter_T_loss','red_fighter_T_draws','blue_fighter_name','blue_fighter_result','blue_fighter_T_wins','blue_fighter_T_loss','blue_fighter_T_draws',]
csv_file=open('sherdog.csv', 'w', encoding="utf-8", newline='')
writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
writer.writeheader()

class sherdog(scrapy.Spider):
    name = 'sherdog'
    title = 'Sherdog'
    start_urls = ['https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2']

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


    def parse(self,response):
        links=response.css('#recent_tab tr td a[itemprop="url"]::attr(href)').extract()
        for link in links:
            Nlink='https://www.sherdog.com{}'.format(link)
            yield scrapy.Request(Nlink, callback=self.parse_events)

        if(response.css('.pagination a::text').extract_first()[:5]=='Older'):
            pagination='https://www.sherdog.com{}'.format(response.css('.pagination a::attr(href)').extract_first())
            yield scrapy.Request(pagination)


    def parse_events(self,response):
        item=dict()
        item['match_date']=datetime.strptime(response.css('.info span[class="date"]::text').extract_first(), "%b %d, %Y").strftime('%m/%d/%Y')
        item['red_fighter_name']=response.css('.col_left section[itemprop="subEvent"] .fight .fighter.left_side h3 span[itemprop="name"]::text').extract_first()
        item['red_fighter_T_wins']=response.css('.col_left section[itemprop="subEvent"] .fight .fighter.left_side span[class="record"]::text').extract_first().split(" - ")[0]
        item['red_fighter_T_loss']=response.css('.col_left section[itemprop="subEvent"] .fight .fighter.left_side span[class="record"]::text').extract_first().split(" - ")[1]
        item['red_fighter_T_draws']=response.css('.col_left section[itemprop="subEvent"] .fight .fighter.left_side span[class="record"]::text').extract_first().split(" - ")[2]

        item['blue_fighter_name'] = response.css('.col_left section[itemprop="subEvent"] .fight .fighter.right_side h3 span[itemprop="name"]::text').extract_first()
        item['blue_fighter_T_wins'] = response.css('.col_left section[itemprop="subEvent"] .fight .fighter.right_side span[class="record"]::text').extract_first().split(" - ")[0]
        item['blue_fighter_T_loss'] = response.css('.col_left section[itemprop="subEvent"] .fight .fighter.right_side span[class="record"]::text').extract_first().split(" - ")[1]
        item['blue_fighter_T_draws'] = response.css('.col_left section[itemprop="subEvent"] .fight .fighter.right_side span[class="record"]::text').extract_first().split(" - ")[2]

        writer.writerow(item)
        yield item
