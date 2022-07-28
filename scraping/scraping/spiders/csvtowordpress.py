#alpha1133 p$08HbZXVsjZ4@S*2iEytXE0
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts
file=open('data.csv','r')
data=file.read().split('\n')
title=[]
content=[]
for i in data:
    i=i.split(',')
    try:
        title.append(i[0])
        content.append(i[1])
        # print(content)
    except:
        pass
print( title[:-1])

client=Client('https://realzz.nl/xmlrpc.php','realzz','GVgQNJWzG%b#xFlHa0QTAW@x')
# myblog=client.call((posts.GetPosts()))
# print(myblog)
postx=WordPressPost()
for k in title[:-1]:
    postx.title = k
for j in content:
    postx.content=j
postx.post_status = 'publish'
client.call(posts.NewPost(postx))
