import csv

if __name__ == '__main__':
    headers = ['sku', 'name']
    csv_file = open('skus I couldnt find on stockx.csv', 'w', newline='', encoding='utf-8')
    csvwriter = csv.DictWriter(csv_file, fieldnames=headers)
    csvwriter.writeheader()
    file = open('unmatchednamesorskus.txt','r', encoding='utf-8')
    txtfile = file.read().split('\n')

    for txt in txtfile:
        item = dict()
        item['sku'] = txt.split('*')[0]
        item['name'] = txt.split('*')[1]
        csvwriter.writerow(item)
        csv_file.flush()