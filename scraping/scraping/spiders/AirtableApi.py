try:
    import pkg_resources.py2_warn
except ImportError:
    pass
import json
import logging

import requests

DATE_FMT = "%Y-%m-%d"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "https://api.airtable.com/v0"


class AirtableClient:
    def __init__(self, api_key, base_key):
        self.api_key = api_key
        self.base_key = base_key

    def __headers(self):
        return {"Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"}

    def search_record(self,table_name, searchurl, fcol):
        global iid
        url = BASE_URL + '/' + self.base_key + "/" + table_name
        querystring = {"filterByFormula": "({"+fcol+"}=" + f"\"{searchurl}\")"}
        response = requests.get(url=url, headers=self.__headers(),params=querystring)
        if len(json.loads(response.text).get('records'))!=0:
            iid = json.loads(response.text).get('records')[0].get('id')
            alreadyexists = True
        else:
            alreadyexists = False
        return alreadyexists

    def insert_records(self, table_name, records,fcol):
        responses = []
        for chunk in self.chunks(items=records, size_of_chunks=10):
            data = {"records": []}
            dat = {"records": []}
            for item in chunk:
                exists = self.search_record(table_name,item[fcol], fcol)
                if exists == True:
                    dat["records"].append({"id":iid,"fields": item})
                else:
                    data["records"].append({"fields": item})
            if len(data['records']) != 0:
                url = BASE_URL + '/' + self.base_key + "/" + table_name
                logger.info(f"sending to {url}")
                response = requests.post(url=url, json=data, headers=self.__headers())
                responses.append(response.json())
            else:
                logger.info(f"Data Already Exists")
            if len(dat["records"])!=0:
                url = BASE_URL + '/' + self.base_key + "/" + table_name
                response = requests.patch(url=url, json=dat, headers=self.__headers())

    def chunks(self, items, size_of_chunks):
        for i in range(0, len(items), size_of_chunks):
            chunk = items[i:i + size_of_chunks]
            logger.info(f"Created chunk {len(chunk)}")
            yield chunk
