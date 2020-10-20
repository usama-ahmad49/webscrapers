import json
import csv
import scrapy

csvheaders=['year', 'make', 'model', 'trim', 'mileage','tag', 'price']
file=open('shiftScraper.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(file,fieldnames=csvheaders)
writer.writeheader()

headers={'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'en-US,en;q=0.9','cache-control':'no-cache','cookie':'session=MTYwMjUwNTkzOXxpRFdqNl9pcHJoT1ptUW1BNTB4bGJ5b2l0djlpQlJleUJsSnE1R0FZdnViTWg0NFhaNE1JTGZUbjJ4S3hmUHlod1I0SllVZjRmMU53VmVPYU1YZldfVUNMX1c0SkJfRjZMQjltUkg2YXBvT2JVXzZIWlh3WS1nTnlPRGJ5ZUtOWWNRTk8xbjVYeUgxVzFPQ2dBZDMxOEllTWJHNWxhT1VTMGwzMEtvYjlWQnlqRFl2cm5zTT18dzhoecS-xJuiSd9SRKcods0jVpu_DvudnpdOHHPt3Lk=; ajs_anonymous_id=%221ef05755-478c-404a-84e6-800502cce31f%22; region=us/or1; ajs_anonymous_id=%221ef05755-478c-404a-84e6-800502cce31f%22; _ga=GA1.2.1341473980.1602505942; _gid=GA1.2.270640763.1602505942; _gcl_au=1.1.1003522921.1602505943; _fbp=fb.1.1602505943777.217316341; wcsid=MI4zJx4Y3MXyh1Sm8a5TS0KBV6rN4LIj; hblid=E4n6CGsos9GNMX1s8a5TS0KNoLB4rakV; _okdetect=%7B%22token%22%3A%2216025059443580%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22shift.com%22%7D; fs_uid=rs.fullstory.com#27E7E#4633735859847168:6285142799204352/1634041943; olfsk=olfsk6492480372377907; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1602505944918%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=7897-289-10-5368; __adroll_fpc=937e673548011cad5ee5e15928e50b5e-1602505945114; tatari-session-cookie=4e35589b-4e35-c671-6293-54cf8f9a767a; tatari-user-cookie=1ef05755-478c-404a-84e6-800502cce31f; pxa_id=qwKLlO6qcpvNmFjG2hKE2jnn; pxa_at=true; _sp_id.608c=39aeecb9-e4fc-4362-82db-7540620684d4.1602505942.2.1602509717.1602506675.f50c2bf1-2cd4-4fee-8c06-90efd60547b3; _sp_ses.608c=*; _gat=1; _oklv=1602509722221%2CMI4zJx4Y3MXyh1Sm8a5TS0KBV6rN4LIj; __ar_v4=NUOJO4NABVCOZEGYYR3XDH%3A20201011%3A5%7C4WHX622MNRGCHMRESNXGEI%3A20201011%3A5%7CPKHHLDA4DVA7VCJNZEBJ5X%3A20201011%3A4%7CRZSHOI3AUVGBZPEHYHWWMC%3A20201011%3A1; tatari-cookie-test=29912425; t-ip=1; _uetsid=fa850eb00c8611eb8cdecf7fb77d4a06; _uetvid=fa8546600c8611ebaf965b1fe7a807dc; _dd_s=rum=1&id=7ff0030c-d35d-4fa5-bda2-b22cb41fad89&created=1602509716747&expire=1602510659871',
         'pragma':'no-cache','referer':'https://shift.com/cars/oregon','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin','shift-envelope-base':'{"analytics_info":{"context":{"campaign":{"content":null,"medium":null,"name":null,"source":null,"term":null},"page":{"path":"/cars/oregon","referrer":"","search":"","title":"Used cars for sale in Oregon | Shift","url":"https://shift.com/cars/oregon"}},"google_click_identifier":null},"app_info":{"app_identifier":"ConsumerWeb","app_version":"1.0.2","build":"2020-10-10T06:00:39Z_bk-gae-24117"},"client_info":{"locale":"en-US","os_name":"Win32","os_version":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}}',
         'shift-envelope-request-id':'JNh9WDnECEn','shift-envelope-timestamp':'2020-10-12T13:36:00.285Z','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
         'x-requested-with':'XMLHttpRequest',}


class shitfScraper(scrapy.Spider):
    name = 'shitfcraper'
    title = 'ShitfScraper'
    start_urls = ['https://shift.com/cars/oregon']

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
        yield scrapy.Request(url='https://shift.com/clientapi/consumer/buyer/get_slim_cars_by_zip_1?request=%7B%22zip_code%22%3A%2202112%22%7D', callback=self.parse,headers=headers)

    def parse(self, response):
        start_json = response.text
        # json_str = start_json[:start_json.find('</script')]
        json_data = json.loads(start_json)
        for car in self.get_dict_value(json_data, ['result', 'content','cars'], []):
            item = dict()
            try:
                item['year'] = car.get('year')
            except:
                item['year']=''
            try:
                item['make'] = car.get('make')
            except:
                item['make'] =''
            try:
                item['model'] = car.get('model')
            except:
                item['model'] =''
            try:
                item['trim'] = car.get('trim')
            except:
                item['trim'] = ''
            try:
                item['mileage'] = car.get('mileage')
            except:
                item['mileage'] =''
            try:
                item['price'] = car.get('price') #self.get_dict_value(car, ['price', 'total'])
            except:
                item['price'] =''
            try:
                item['tag'] = car.get('tags',[])[0]
            except:
                item['tag'] =''
            writer.writerow(item)
            file.flush()

        yield item
