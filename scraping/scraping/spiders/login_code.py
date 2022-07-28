import csv
import json
import time
from datetime import datetime,timedelta
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from seleniumwire import webdriver

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("wowprojects-fc84dea2858c.json", scope)
client = gspread.authorize(creds)
sheet = client.open("NetworkHealthDetail").sheet1

# year month day
from_date = str(datetime.now()-timedelta(days=1))
to_date = str(datetime.now()-timedelta(days=1))

driver = webdriver.Chrome()
email = 'anthony.rumph@wowinc.com'
password = 'qwerty1234'
driver.maximize_window()
driver.get('https://wow.deepfield.net/login')
driver.find_element_by_name('email').send_keys(email)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/form/div[2]/button').click()
time.sleep(2)
print('login done')
links_file = open('links.txt', 'r', encoding='utf-8')
links = links_file.read().split('\n')
links = [l for l in links if l.strip()]
i = 1
data = sheet.get_all_records()
if len(data)>1:
    i = len(data)+1
videoinsertRowlist = []
gameinsertRowlist = []
VCinsertRowlist = []
CMTSinsertRowlist = []
for link in links:
    csvheaders = ['Category', 'CMTS', 'Received bps (P95)', 'Sent bps (P95)']
    file = open('data-{}.csv'.format(link.split('=')[1]), 'w', newline='', encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=csvheaders)
    writer.writeheader()
    driver.get(link)
    time.sleep(15)
    got_data = False
    while not got_data:
        try:
            req = [v for v in driver.requests if 'eld.net/cube/big_cube.json?slice=timestamp' in v.url and 'dimensions=category,' in v.url and '&estimate=' not in v.url][0]
            got_data = True
        except:
            time.sleep(1)

    headers = dict(req.headers)
    # https://wow.deepfield.net/report/601?__=fff4f8601d07db39 1
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T08-00:{}T17-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=category,cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&slice=category(3,1)&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['44']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[1]:
                item = dict()
                item['Category'] = type_[cube[0]] + ' 08:00 to 17:00'
                item['CMTS'] = v['name']
                item['Received bps (P95)'] = cube[2]
                item['Sent bps (P95)'] = cube[3]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                if type_[cube[0]] == 'video':
                    videoinsertRowlist.append(insertRow)
                else:
                    gameinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()
    # https://wow.deepfield.net/report/601?__=fff4f8601d07db39 2
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T17-00:{}T23-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=category,cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&slice=category(3,1)&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['44']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[1]:
                item = dict()
                item['Category'] = type_[cube[0]] + ' 17:00 to 23:00'
                item['CMTS'] = v['name']
                item['Received bps (P95)'] = cube[2]
                item['Sent bps (P95)'] = cube[3]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                if type_[cube[0]] == 'video':
                    videoinsertRowlist.append(insertRow)
                else:
                    gameinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()
    # https://wow.deepfield.net/report/597?__=471051fcab751f9b   1
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T08-00:{}T17-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&slice=sites(54697,399,1442,998,3495)&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['22328']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[0]:
                item = dict()
                item['Category'] = 'video conference 08:00 to 17:00'
                item['CMTS'] = type_[cube[0]]
                item['Received bps (P95)'] = cube[1]
                item['Sent bps (P95)'] = cube[2]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                VCinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()
    # https://wow.deepfield.net/report/597?__=471051fcab751f9b 2
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T17-00:{}T23-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&slice=sites(54697,399,1442,998,3495)&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['22328']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[0]:
                item = dict()
                item['Category'] = 'video conference 17:00 to 23:00'
                item['CMTS'] = type_[cube[0]]
                item['Received bps (P95)'] = cube[1]
                item['Sent bps (P95)'] = cube[2]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                VCinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()
    # https://wow.deepfield.net/report/596?__=317c5b800f030782   1
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T08-00:{}T17-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['22328']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[0]:
                item = dict()
                item['Category'] = 'cmts 08:00 to 17:00'
                item['CMTS'] = type_[cube[0]]
                item['Received bps (P95)'] = cube[1]
                item['Sent bps (P95)'] = cube[2]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                CMTSinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()
    # https://wow.deepfield.net/report/596?__=317c5b800f030782 2
    url = 'https://wow.deepfield.net/cube/big_cube.json?slice=timestamp({}T17-00:{}T23-00)&tz=MST7MDT&apply=timestep(5min)&dimensions=cmts.local&measures=pctl95.recv.bps,pctl95.sent.bps&slice=sites(54697,399,1442,998,3495)&apply=inline_ddb()&apply=convert_to_names!()&apply=return_dimension_names!()'.format(from_date, to_date)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    all_data = []
    type_ = {k['position_id']: k['name'] for k in data['dimensions_db']['22328']['positions'].values()}
    for v in data['dimensions_db']['22328']['positions'].values():
        for cube in data['cube']:
            if v['position_id'] == cube[0]:
                item = dict()
                item['Category'] = 'cmts 17:00 to 23:00'
                item['CMTS'] = type_[cube[0]]
                item['Received bps (P95)'] = cube[1]
                item['Sent bps (P95)'] = cube[2]
                item['CMTS'] = from_date
                insertRow = [item['Category'], '', '', item['CMTS'], item['Received bps (P95)'], item['Sent bps (P95)'],item['CMTS']]
                CMTSinsertRowlist.append(insertRow)
                writer.writerow(item)
                file.flush()

    for game in gameinsertRowlist:
        i+=1
        time.sleep(3)
        sheet.insert_row(game,i)
    for video in videoinsertRowlist:
        i += 1
        time.sleep(3)
        sheet.insert_row(video, i)
    for vc in VCinsertRowlist:
        i += 1
        time.sleep(3)
        sheet.insert_row(vc, i)
    for cmts in CMTSinsertRowlist:
        i += 1
        time.sleep(3)
        sheet.insert_row(cmts, i)
