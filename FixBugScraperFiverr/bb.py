import sys
from bs4 import BeautifulSoup
import urllib.request as req
import pandas as pd
import time
start_time = time.time()


def f(string):
    return str(string[0] + ', ' + string[-1])



rooturl = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/"
url = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_1=prov_1&progNameOnly=N&start=0&finish=200&section=1"

page = req.urlopen(url)

soup = BeautifulSoup(page,'html.parser')

#Using indirect | clash removed
info = soup.find_all("div", class_="wb-frm")
names = [x.form.div.find_all("li") for x in info][0]
names2 = [names[i:i + 3] for i in range(0, len(names)-12, 3)]


#Filling all names in diploma variable
diploma = [[x[0].findAll("a")[0].find(text=True).strip(), x[1].string, f(x[2].find(text=True).strip().split())] for x in
           names2]

#Gathering relative links and converting to absolute
links = [x.ol.find_all("a") for x in info][0]
links2 = [y.get('href') for y in links]
links3 = [rooturl + z for z in links2]

#Iterate over all link and fetch data for all
for i in range(len(links3)):
    url_link = req.urlopen(links3[i])
    link_html = BeautifulSoup(url_link,"html.parser")
    link_html2 = link_html.find_all("div", class_="panel-body")
    website = link_html2[1].a.get('href')
    diploma[i].append(website)

#Fetching dt/dd data & filling a dict.
    infoOne = [];infoTwo = []
    for d in link_html2[3].find_all('dd'):
        if d.a is not None:
            infoOne.append(d.a.string)
            continue
        if d.string is not None:
            infoOne.append(d.string)
            continue
        infoOne.append(d.text)

    for d in link_html2[3].find_all('dt'):
        if d.string is not None:
            infoTwo.append(d.string)
            continue
        infoTwo.append('n/a')



    general_info = dict(zip(infoTwo,infoOne))
    print("Scraped page no. - " + str(i))
    #Filing Dict to complete Set
    diploma[i].append(general_info)


col1 = [x[1] for x in diploma]
col2 = [x[0] for x in diploma]
col3 = [x[2] for x in diploma]
col4 = [x[3] for x in diploma]
col5 = [x[4] for x in diploma]

#Fake coll.
col55 = {'Program Level': [x.get('Program Level:') for x in col5],
         'Credential Type': [x.get('Credential Type:') for x in col5],
         'Joint Program Level': [x.get('Joint Program Level:') for x in col5],
         'Joint Credential Type': [x.get('Joint Credential Type:') for x in col5],
         'Address': [x.get('Address:') for x in col5],
         'Telephone': [x.get('Telephone:') for x in col5],
         'Email': [x.get('Email:') for x in col5],
         'Fax': [x.get('Fax:') for x in col5],
         'Toll Free': [x.get('Toll Free:') for x in col5]
         }

#Data Frame one initialized
df = pd.DataFrame(col1, columns=['University'])
#Data Frame two just conversion
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

print("SUCCESS!! --- %s seconds were consumed by Flash ---" % (time.time() - start_time))
