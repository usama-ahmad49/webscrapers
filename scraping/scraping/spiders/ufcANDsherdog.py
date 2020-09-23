import csv

ufc_file = open('ufcdata.csv', 'r')
csv_reader = csv.DictReader(ufc_file, delimiter=',')

for data in csv_reader.split('\n')[1:]:
    list = data.split(',')
    match_date=list[1]
