import csv

if __name__ == '__main__':
    filein = open('Stock X missing images Batch 2.csv','r',encoding='utf-8')
    fileout = open('Stock X missing images Batch 2.txt','w',encoding='utf-8')
    csvwriter = csv.DictReader(filein)
    for v in csvwriter:
        string = v['Skus']+'*'+v['Names']
        fileout.write(string+'\n')