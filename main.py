from bs4 import BeautifulSoup as bs 
import requests
import os
from random import randint
import json
account = ""
password = ""


def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)
    

def dlBoard(url):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    req = requests.get(url,headers)
    soup = bs(req.content, 'html.parser')
    soup.prettify()
    trueimg = soup.select('script#__PWS_DATA__')[0].text.strip()
    print(trueimg)
    js = json.loads(trueimg)
    rs = 10**(8-1)
    re = (10**8)-1
    dname = randint(rs,re)
    os.makedirs(str(dname))
    originals = []
    for i in item_generator(js,'orig'):
        val = {"og":i}
        originals.append(val['og'])
    seen = []
    for i in originals:
        if isinstance(i,dict):
            print(i['url'])
            if(i['url'] not in seen):
                idatum = requests.get(i['url']).content
                rs = 10**(6-1)
                re = (10**6)-1
                iname = str(randint(rs,re))
                with open(os.path.join(str(dname) + "/" + str(iname) +".png"),'wb') as path:
                    path.write(idatum)
                    seen.append(i['url'])

print("give a board url:")
url = input()
dlBoard(url)


