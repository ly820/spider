#!/usr/bin/env python3
#!-*- encoding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost',27017)
tripadvisor_database = client['tripadvisor_table']
sights_sports = tripadvisor_database['sights_sports']

def get_sights_sport_infomation(url):
    """
        @url: 想要获取网页地址
        该函数返回给出地址的所有景点信息，以及景点的详细信息的url
    """

    web_data = requests.get(url)  # 请求服务器，获得响应信息
    soup = BeautifulSoup(web_data.text,"lxml")  # 将获取的网页信息转换成BeautifulSoup对象，便于以后处理
    titles = soup.select("div.property_title > a[target=_blank]")  # 景点的标题
    tags = soup.select("div.p13n_reasoning_v2")   # 景点的标签（属于哪类景点，寺庙，城堡之类的）
    rates = soup.select("span.rate.rate_no > img")  # 景点的评分
    #infomation_of_sight_sports = []   # 构造一个列表，用来存储该页所有的景点信息
    for title,tag,rate in zip(titles,tags,rates):   # 用zip()函数，同时对所有的选项进行迭代
        # 构造一个字典，存储没一个景点的信息
        item = {
        'tilte':title.get_text(),
        'tag':list(tag.stripped_strings),
        'rate':rate.get('alt'),
        'url_info':'http://www.tripadvisor.cn/'+title.get('href')   # 该景点详细信息的url
        }
        sights_sports.insert_one(item)
        #infomation_of_sight_sports.append(item)
    #return infomation_of_sight_sports
    return None
if __name__ == "__main__":
    url = "http://www.tripadvisor.cn/Attractions-g293916-Activities-Bangkok.htm"
    #items = get_sights_sport_infomation(url)
    #for item in items :
    #   print(item)
    get_sights_sport_infomation(url)
    for item in sights_sports.find():
        print(item)
