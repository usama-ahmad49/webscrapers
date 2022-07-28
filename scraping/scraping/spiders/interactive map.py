import folium
import pandas as pd
import csv
from geopy.geocoders import Nominatim

# my_map = folium.Map(
#     zoom_start= 2
# )
#
# cities = pd.read_csv('BedsandBars.csv')
#
# city = cities.loc[0]
# folium.Marker(
#     location=[city['City']]
# ).add_to(my_map)


headers = ["Venue Group","Venue Name","City","Country","Full Address","Lat n long"]
fileoutput = open('interactivemaps.csv','w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileoutput, fieldnames=headers)
csvwriter.writeheader()

geolocator = Nominatim(user_agent = "example")
file = open('vanuesandbars.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(file, delimiter=',')
line_count = 0
for row in csv_reader:
    if line_count == 0:
        # print(f'Column names are {", ".join(row)}')
        line_count += 1
        continue
    item = dict()
    address = row[-1].strip()
    i=0
    while i<3:
        loc = geolocator.geocode(address)
        if loc != None:
            break
        elif i==0:
            address = address.split(',')[0]
        elif i == 1:
            try:
                address = address.split(',')[1]
            except:
                address = address.split(',')[-1]
        elif i ==2:
            try:
                address = address.split(',')[2]
            except:
                address = address.split(',')[-1]
        i+=1
    if loc != None:
        item['Venue Group'] = row[0]
        item['Venue Name'] = row[1]
        item['City'] = row[2].strip()
        item['Country'] = row[3]
        item['Full Address'] = row[4]
        item['Lat n long'] = [loc.latitude, loc.longitude]
        csvwriter.writerow(item)
        fileoutput.flush()


