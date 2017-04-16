# coding: utf-8
#All imports here
import urllib2 #Making URL requests
from bs4 import BeautifulSoup  #HTML Parsing
import sys
import pandas as pd  #Changing data to dataframe and saving as CSV
import time
start_time = time.time()


#functions used
def f(string):
    return str(string[0] + ', ' + string[1])



url = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_1=prov_1&progNameOnly=N&start=0&finish=4&section=1"
rooturl = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/"


page = urllib2.urlopen(url)

#Reloading & Configuring system
reload(sys)
sys.setdefaultencoding('utf-8')


soup = BeautifulSoup(page,"html.parser")
info = soup.find_all("div", class_="wb-frm")

names = [x.find_all("li",class_='mrgn-tp-md') for x     in info][0]


print(names)
names2 = [names[i:i + 3] for i in range(0, len(names), 3)]




for x in names2:
    a= x[0].findAll("a")[0].find(text=True).strip()
    b=x[1].string
    c=x[2].find(text=True).strip().split()
    print('--------tctctksdvbsbv--------------')
    print(a)
    print(b)
    print(c)
    print('----===sdvbsjdvbsjh==---------')


diploma = [[x[0].findAll("a")[0].find(text=True).strip(), x[1].string, f(x[2].find(text=True).strip().split())] for x in
           names2]

print('3')

links = [x.ol.find_all("a") for x in info][0]
links2 = [y.get('href') for y in links]
links3 = [rooturl + z for z in links2]

print('Real diploma before hitting there')
print(diploma)
print('\n\n')


for i in xrange(len(links3)):
    url_link = urllib2.urlopen(links3[i])
    print('link opened')
    link_html = BeautifulSoup(url_link,"html.parser")
    link_html2 = link_html.find_all("div", class_="panel-body")
    website = link_html2[1].a.get('href')
    diploma[i].append(website)
    print(website)
    print('website')

#Fetching dt/dd data in filling dict.
    infoOne = [];infoTwo = []


    for d in link_html2[3].find_all('dd'):
        if d.a is not None:
            infoOne.append(d.a.string)
            continue

        if d.string is not None:
            infoOne.append(d.string)
            continue

        infoOne.append('n/a')

    for d in link_html2[3].find_all('dt'):
        if d.string is not None:
            infoTwo.append(d.string)
            continue

        infoTwo.append('n/a')

    print('\n\n');print(infoOne);print(infoOne);print('\n\n')
    general_info = dict(zip(infoOne,infoTwo))
    print("Scraped page no. - " + str(i))
    print('diploma value new one - ')
    print(diploma[i])
    #Filing Dict to complete Set
    diploma[i].append(general_info)

col1=col2=col3=col4=[]
col5={}


col1 = [x[1] for x in diploma]
col2 = [x[0] for x in diploma]
col3 = [x[2] for x in diploma]
col4 = [x[3] for x in diploma]
col5 = [x[4] for x in diploma]

print(col5)

#Creating Item details to fill complete Set
col55 = {'Program Level': [col5.get('Program Level:')],
         'Credential Type': [col5.get('Credential Type:')] ,
         'Joint Program Level': [col5.get('Joint Program Level:') ],
         'Joint Credential Type': [col5.get('Joint Credential Type:')],
         'Address': [col5.get('Address:')],
         'Telephone': [col5.get('Telephone:') ],
         'Email': [col5.get('Email:') ],
         'Fax': [col5.get('Fax:') ],
         'Toll Free': [col5.get('Toll Free:') ]
         }

print("Col55 data")
print(col55)

df = pd.DataFrame(col1, columns=['University'])


df2 = pd.DataFrame(col55)


df['Type'] = col2
df['City'] = col3
df['Website'] = col4
df['Address'] = df2['Address']
df['Credential Type'] = df2['Credential Type']
df['Email'] = df2['Email']
df['Fax'] = df2['Fax']
df['Joint Credential Type'] = df2['Joint Credential Type']
df['Joint Program Level'] = df2['Joint Program Level']
df['Program Level'] = df2['Program Level']
df['Telephone'] = df2['Telephone']
df['Toll Free'] = df2['Toll Free']


df.to_csv('ABdata1.csv', encoding='utf-8')


# coding: utf-8

# In[280]:
#
# import urllib2
#
# url = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_4=prov_4&progNameOnly=N&start=1000&finish=1999&section=2"
# page = urllib2.urlopen(url)
#
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# # In[282]:
#
# rooturl = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/"
#
# # In[283]:
#
# from bs4 import BeautifulSoup
#
# # In[284]:
#
# soup = BeautifulSoup(page)
#
# # In[285]:
#
# info = soup.find_all("div", class_="cl-content")
#
# # In[286]:
#
# names = [x.ol.find_all("li") for x in info][0]
#
#
# # In[289]:
#
# def f(string):
#     return str(string[0] + ', ' + string[-1])
#
#
# # In[290]:
#
# names2 = [names[i:i + 3] for i in range(0, len(names), 3)]
#
# # In[291]:
#
# diploma = [[x[0].findAll("a")[0].find(text=True).strip(), x[1].string, f(x[2].find(text=True).strip().split())] for x in
#            names2]
#
# # In[297]:
#
# links = [x.ol.find_all("a") for x in info][0]
#
# # In[294]:
#
# links2 = [y.get('href') for y in links]
#
# # In[295]:
#
# links3 = [rooturl + z for z in links2]
#
# # In[296]:
#
# for i in xrange(len(links3)):
#     url_link = urllib2.urlopen(links3[i])
#     link_html = BeautifulSoup(url_link)
#     link_html2 = link_html.find_all("div", class_="span-4 row-end")
#     website = link_html2[0].a.get('href')
#     diploma[i].append(website)
#
#     general_info_html = link_html.find_all("div", class_="grid-12 equalize cl-border-top-dot")
#     general_info_html2 = [y.findAll('div') for y in general_info_html[1:]]
#     general_info = {}
#     for x in general_info_html2:
#         general_info.update({x[0].find(text=True): x[1].find(text=True)})
#     diploma[i].append(general_info)
#
# # In[298]:
#
# import pandas as pd
#
# # In[300]:
#
# col1 = [x[1] for x in diploma]
# col2 = [x[0] for x in diploma]
# col3 = [x[2] for x in diploma]
# col4 = [x[3] for x in diploma]
# col5 = [x[4] for x in diploma]
#
# # In[301]:
#
# col55 = {'Program Level': [x.get('Program Level:') for x in col5],
#          'Credential Type': [x.get('Credential Type:') for x in col5],
#          'Joint Program Level': [x.get('Joint Program Level:') for x in col5],
#          'Joint Credential Type': [x.get('Joint Credential Type:') for x in col5],
#          'Address': [x.get('Address:') for x in col5],
#          'Telephone': [x.get('Telephone:') for x in col5],
#          'Email': [x.get('Email:') for x in col5],
#          'Fax': [x.get('Fax:') for x in col5],
#          'Toll Free': [x.get('Toll Free:') for x in col5]
#          }
#
# # In[311]:
#
# df = pd.DataFrame(col1, columns=['University'])
#
# # In[312]:
#
# df2 = pd.DataFrame(col55)
#
# # In[313]:
#
# df['Type'] = col2
# df['City'] = col3
# df['Website'] = col4
# df['Address'] = df2['Address']
# df['Credential Type'] = df2['Credential Type']
# df['Email'] = df2['Email']
# df['Fax'] = df2['Fax']
# df['Joint Credential Type'] = df2['Joint Credential Type']
# df['Joint Program Level'] = df2['Joint Program Level']
# df['Program Level'] = df2['Program Level']
# df['Telephone'] = df2['Telephone']
# df['Toll Free'] = df2['Toll Free']
#
# # In[320]:
#
# df.to_csv('BCdata2.csv', encoding='utf-8')
#
