import csv
import scrapy
import requests

header1=['movie name','movie link']
header2=['movie name','Primär','Zusätzlich']
file_List_Page_Fields=open('ListPageFields.csv','w',newline='',encoding='utf-8')
writer1=csv.DictWriter(file_List_Page_Fields,fieldnames=header1)
writer1.writeheader()

file_Detail_Page_Field=open('DetailPageField.csv','w',newline='',encoding='utf-8')
writer2=csv.DictWriter(file_Detail_Page_Field,fieldnames=header2)
writer2.writeheader()

def getmovies(url):
    response=requests.get(url=url)
    resp=scrapy.Selector(text=response.content.decode('utf-8'))
    for aplaData in resp.css('#selectedgenre .list.alpha li'):
        link=aplaData.css('li a::attr(href)').extract_first()
        response=requests.get(link)
        respo = scrapy.Selector(text=response.content.decode('utf-8'))
        for listpaginate in respo.css('#selectedgenre > ul:nth-child(2) li'):
            link=listpaginate.css('li a::attr(href)').extract_first()
            response = requests.get(link)
            respo = scrapy.Selector(text=response.content.decode('utf-8'))
            for movie in respo.css('#selectedcontent .column.first ul li'):
                item = dict()
                item['movie name'] = movie.css('a::text').extract_first()
                item['movie link'] = movie.css('a::attr(href)').extract_first()
                writer1.writerow(item)
                file_List_Page_Fields.flush()

                detailresponse=requests.get(item['movie link'])
                movieResp=scrapy.Selector(text=detailresponse.content.decode('utf-8'))

                item2=dict()
                item2['movie name'] = item['movie name']
                try:
                    item2['Primär']=movieResp.css('.information-list--episode .information-list__item__definition ::text').extract()[8]
                except:
                    item2['Primär']='-'
                try:
                    item2['Zusätzlich']=movieResp.css('.information-list--episode .information-list__item__definition ::text').extract()[10]
                except:
                    item2['Zusätzlich'] ='-'
                writer2.writerow(item2)
                file_Detail_Page_Field.flush()



if __name__ == '__main__':
    movielist=[
        'https://itunes.apple.com/de/genre/filme-drama/id4406?letter=A',
        'https://itunes.apple.com/de/genre/filme-thriller/id4416?letter=A',
        'https://itunes.apple.com/de/genre/filme-action/id4401?letter=A',
        'https://itunes.apple.com/de/genre/filme-science-fiction-und-fantasy/id4413?letter=A'
    ]
    for movie in movielist:
        print(movie)
        getmovies(movie)