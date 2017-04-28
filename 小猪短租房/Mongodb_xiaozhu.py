#!/usr/bin/env python3.5
#-*- encoding:utf-8 -*-

'''
获取小猪短租房网站的房源信息,提取数据,并存入数据库 MongoDB 中
'''
__author__ = 'YuanLiu'

from bs4 import BeautifulSoup
import requests
import pymongo
import time
import re

# 链接数据库本地客户端,新建一个数据库 xiaozhu,在新建的数据库里创建存储数据的数据表 duanzufang_tab
client = pymongo.MongoClient('localhost',27017)  # 端口号不要写错了,不然链接不上
xiaozhu = client['xiaozhu']
duanzufang_tab = xiaozhu['duanzufang_tab']


#url = 'http://bj.xiaozhu.com/fangzi/5956869116.html'
def get_house_info(url):
    '''
    传入房源的url，以列表的形式返回房子及房主的信息。
    '''
    # price_per_day 不完全是数字组成的字符串, 为了后面查询, 把字符串中的数字替换成''
    # 构造正则表达式的匹配模式 pattern
    pattern = re.compile('[^\d]')

    # 获取网页
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    #print(soup)

    # 获取数据
    title = soup.select('div.pho_info > h4 > em')[0].get_text()
    address = soup.select('div.pho_info > p')[0].get('title')

    price_per_day =''.join(soup.select('div.day_l')[0].stripped_strings)
    price_per_day = re.sub(pattern,'',price_per_day)

    image = soup.select('#detailImageBox > div.pho_show_r > div > ul > li:nth-of-type(2) > img')[0].get('data-src')
    house_ower_img = soup.select('div.member_pic > a > img')[0].get('src')
    sex_ower = '男' if soup.select('div.member_ico') else '女'
    #if soup.select('div.member_ico'):
    #    sex = '男'
    #else:
    #    sex = '女'
    house_ower_name = soup.select('.lorder_name')[0].get_text()
    # 将数据存储到字典中,然后返回字典
    data = {
        'title' : title,
        'address' : address,
        'price_per' : int(price_per_day),
        'image' : image,
        'house_ower_img' : house_ower_img,
        'sex_ower' : sex_ower,
        'house_ower_img' : house_ower_name
    }
    return data

#a = get_house_info(url)
#print(a)

def get_house_url(num=10):
    '''
    #@ num: 你想获得的页数
    #返回10页所有的房源的地址
    '''

    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,num+1)]
    url_list = []
    for url in urls:
        #time.sleep(2)
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        house_urls = soup.select('a.resule_img_a')
        for house in house_urls:
            url_list.append(house.get('href'))

    return url_list

def lookup_data():
    ''' 查询数据'''
    for item in duanzufang_tab.find({'price_per':{'$gte':500}}):
        print(item)

def start():
    '''
    开始程序,包含程序的主程序
    '''
    # 获得所有房源的url地址
    urls = get_house_url()
    i = 1
    # 遍历每一个房源的url,获取需要的信息
    for url in urls:
        print('正在保存第%s个房源信息'%i)
        time.sleep(2)
        data = get_house_info(url)
        # 在数据表中存储data
        duanzufang_tab.insert_one(data)
        i += 1
    print('保存完毕，可以去数据库中查看')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('一晚上住宿费大于500的房源信息如下：')
    lookup_data()
    client.close()

if __name__ == '__main__':
    start()