#!/usr/bin/env python3
#!-*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pymongo


client = pymongo.MongoClient('localhost',27017)
tripadvisor_database = client['tripadvisor_table']
address_table = tripadvisor_database['address']

url = 'http://www.tripadvisor.cn/Jingdian'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
addresses = soup.select('li.dest-item > a')
for address in addresses:
    item = {
        'address':address.get_text().strip(),
        'url':'http://www.tripadvisor.cn' + address.get('href')
    }
    print(item)
    address_table.insert_one(item)