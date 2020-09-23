import csv

import scrapy
from datetime import datetime

csv_columns = ['match_date', 'red_fighter_name', 'red_fighter_T_wins', 'red_fighter_T_loss',
               'red_fighter_T_draws', 'blue_fighter_name', 'blue_fighter_T_wins',
               'blue_fighter_T_loss', 'blue_fighter_T_draws', ]
csv_file = open('MMAdotcomrenew.csv', 'w', encoding="utf-8", newline='')
writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
writer.writeheader()


class mixedmartialarts(scrapy.Spider):
    name = 'mixedmartialarts'
    title = 'MixedMartialArts'
    start_urls = ['https://www.mixedmartialarts.com/events/search?search=UFC']

    def parse(self, response):
        events = response.css('#event-upcoming tbody tr')

        for event in events:
            link = event.css('td a ::attr(href)').extract_first()
            if (link):
                yield scrapy.Request(link, callback=self.parse_events)

        # if (response.css('.pagination a::text').extract_first()[:5] == 'Older'):
        #     pagination = 'https://www.sherdog.com{}'.format(response.css('.pagination a::attr(href)').extract_first())
        #     yield scrapy.Request(pagination)

    def parse_events(self, response):
        player_links = response.css(
            '#event-panel .fight-item .row .row.names .col-sm-4.col-xs-10.hidden-xs a::attr(href)').extract()

        # player_link='https://www.mixedmartialarts.com/fighter/Greg-Stott:DCE680B8491FEE3C'
        # yield scrapy.Request(player_link, callback=self.parse_Players)
        for player_link in player_links:
            if (player_link):
                yield scrapy.Request(player_link, callback=self.parse_Players)

    def parse_Players(self, response):
        fights = response.css('.table.table-striped.dataTable.responsive.fighter-record tbody tr')
        for fight in fights:
            item = dict()
            item['red_fighter_name'] = response.css('h1[class="newsHeader"] ::text').extract_first().encode('ascii','ignore').decode('utf-8')
            if fight.css('td::text').extract_first() ==' ':
                item['match_date'] = fight.css('td::text').extract()[2]
                item['red_fighter_T_wins'] = fight.css('td::text').extract()[5].split('-')[0][1:]
                item['red_fighter_T_loss'] = fight.css('td::text').extract()[5].split('-')[1]
                item['red_fighter_T_draws'] = fight.css('td::text').extract()[5].split('-')[2].replace(')', '').strip()
                item['blue_fighter_name'] = fight.css('td a::text').extract_first().encode('ascii','ignore').decode('utf-8')
                item['blue_fighter_T_wins'] = fight.css('td::text').extract()[7].split('-')[0][1:]
                item['blue_fighter_T_loss'] = fight.css('td::text').extract()[7].split('-')[1]
                item['blue_fighter_T_draws'] = fight.css('td::text').extract()[7].split('-')[2].replace(')', '').strip()

            elif fight.css('td::text').extract_first()=='NSF':
                item['match_date'] = fight.css('td::text').extract()[1]
                item['red_fighter_T_wins'] = fight.css('td::text').extract()[4].split('-')[0][1:]
                item['red_fighter_T_loss'] = fight.css('td::text').extract()[4].split('-')[1]
                item['red_fighter_T_draws'] = fight.css('td::text').extract()[4].split('-')[2].replace(')', '').strip()
                item['blue_fighter_name'] = fight.css('td a::text').extract_first().encode('ascii','ignore').decode('utf-8')
                item['blue_fighter_T_wins'] = fight.css('td::text').extract()[6].split('-')[0][1:]
                item['blue_fighter_T_loss'] = fight.css('td::text').extract()[6].split('-')[1]
                item['blue_fighter_T_draws'] = fight.css('td::text').extract()[6].split('-')[2].replace(')', '').strip()
            # elif len(fight.css('td::text'))==0:
            #     pass

            else:
                item['match_date'] = fight.css('td::text').extract_first()
                item['red_fighter_T_wins'] = fight.css('td::text').extract()[3].split('-')[0][1:]
                item['red_fighter_T_loss'] = fight.css('td::text').extract()[3].split('-')[1]
                item['red_fighter_T_draws'] = fight.css('td::text').extract()[3].split('-')[2].replace(')', '').strip()
                item['blue_fighter_name'] = fight.css('td a::text').extract_first().encode('ascii','ignore').decode('utf-8')
                item['blue_fighter_T_wins'] = fight.css('td::text').extract()[5].split('-')[0][1:]
                item['blue_fighter_T_loss'] = fight.css('td::text').extract()[5].split('-')[1]
                item['blue_fighter_T_draws'] = fight.css('td::text').extract()[5].split('-')[2].replace(')', '').strip()

            writer.writerow(item)
            csv_file.flush()
