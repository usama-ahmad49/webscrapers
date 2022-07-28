import csv
import os
import mysql.connector


def csvfiles():
    absolutepath = os.path.dirname(os.path.abspath(__file__))
    global path
    path = absolutepath + '\CSVtoMysql'
    files = [v for v in os.listdir(path) if v.endswith('.csv')]
    return files


def inputrows(infile):
    inputrows = []
    for row in infile:
        inputrows.append(row)
    return inputrows

def datafromcsv(rowslist):
    for row in rowslist:
        data = (row['Site'], row['Hosts'], row['Bare'], row['TLD'], row['License'], row['State'], row['Source'], row['Zapped'], row['Burped'])
        query = "insert into DataCsv (Site, Hosts, Bare, TLD, License, State, Source, Zapped, Burped) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(query, data)
        mydb.commit()

if __name__ == '__main__':
    files = csvfiles()
    createQuery = "CREATE TABLE `DataCsv` (`id` int NOT NULL AUTO_INCREMENT,`Site` varchar(200) DEFAULT NULL,`Hosts` varchar(200) DEFAULT NULL,`Bare` varchar(200) DEFAULT NULL,`TLD` varchar(200) DEFAULT NULL,`License` varchar(200) DEFAULT NULL,`State` varchar(200) DEFAULT NULL,`Source` varchar(200) DEFAULT NULL,`Zapped` varchar(200) DEFAULT NULL,`Burped` varchar(200) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        password="123456789",
        user="root",
        database="testfloderschema"
    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute(createQuery)
        mydb.commit()
    except:
        print('Table already created')

    for file in files:
        inputfile = open(path+'\\'+file, 'r', encoding='utf-8-sig')
        infile = csv.DictReader(inputfile)
        rowslist = inputrows(infile)
        print('this')
        datafromcsv(rowslist)

