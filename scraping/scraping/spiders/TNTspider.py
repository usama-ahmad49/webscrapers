import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

header=["shipment_id","consignment_Number","Customer reference","number_Of_Pieces","origin_Address","origin_Date","destination_Address","destination_Date","status"]
fileoutput=open('TNTspiderOutput.csv','w',newline='',encoding='utf-8')
writer= csv.DictWriter(fileoutput,fieldnames=header)
writer.writeheader()

class TNTspider(scrapy.Spider):
    name = 'tntspider'

    @staticmethod
    def read_input():
        inputkeys = []
        file = open('input_TNTspider.txt', 'r')
        for i in file.read().split('\n'):
            inputkeys.append(i)
        return inputkeys

    @staticmethod
    def get_dict_value(data, key_list, default=''):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def start_requests(self):
        inputlist = self.read_input()
        for key in inputlist:
            url = 'https://www.tnt.com/api/v3/shipment?ref={}&locale=en_US&searchType=REF&channel=OPENTRACK'.format(key)
            yield scrapy.Request(url=url, meta={'key': key})

    def parse(self, response):
        item = dict()
        json_data=json.loads(response.text)
        for ind_data in self.get_dict_value(json_data,['tracker.output','consignment'],[]):
            item['shipment_id']=ind_data.get('shipmentId')
            item['consignment_Number']=ind_data.get('consignmentNumber')
            item['Customer reference']=ind_data.get('customerReference')
            item['number_Of_Pieces']=ind_data.get('numberOfPieces')
            item['origin_Address']=self.get_dict_value(ind_data,['originAddress','city'])+', '+self.get_dict_value(ind_data,['originAddress','country'])
            item['origin_Date']=ind_data.get('originDate')
            item['destination_Address']=self.get_dict_value(ind_data,['destinationAddress','city'])+', '+self.get_dict_value(ind_data,['destinationAddress','country'])
            item['destination_Date'] = ind_data.get('destinationDate')
            item['status']=self.get_dict_value(ind_data,['status','groupCode'])
            writer.writerow(item)
            fileoutput.flush()






process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(TNTspider)
process.start()
