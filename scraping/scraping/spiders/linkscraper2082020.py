import csv
import datetime


if __name__ == '__main__':
    file = open('csvfile.csv', 'r')
    reader = csv.DictReader(file)
    datadict = dict()
    for row in reader:
        datadict={row['ï»¿stringID']: {'date': row['date'], 'count': row['count']}}


    stringidnew=input()

    if stringidnew in datadict.keys():
        datadict[stringidnew]['date'] = datetime.date.today()
        datadict[stringidnew]['count'] = datadict[stringidnew]['count'] + 1

    else:
        datadict[stringidnew] = stringidnew
        datadict['id']['date'] = datetime.date.today()
        datadict['id']['count'] = 1