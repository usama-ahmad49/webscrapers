import requests

url = 'https://www.python.org/static/img/python-logo@2x.png'

myfile = requests.get(url)

open('C:/Users/user/Downloads/python.png', 'wb').write(myfile.content)