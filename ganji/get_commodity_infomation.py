#! -*--encoding:utf-8*-
'''
该模块的功能：获取给定商品链接的详细信息
'''

import requests
from bs4 import BeautifulSoup
import pymongo
import time

# 链接数据库
client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
commodity_infomation = ganji['commodity_infomation'] # 存储商品详细信息

# 设置代理
#proxy_list = [
#    'http://101.251.199.66:3128',
#    'http://101.200.40.179:8118',
#    'http://123.117.86.89:9000'
#]
#proxy_ip = random.choice(proxy_list)
#proxies = {'http':proxy_ip}

def get_commodity_infomation(url):

    '''

    :param url: 商品的详情url
    :return: None
    该函数的功能：获取商品详情页面的信息,并存入数据库
    '''

    wb_data = requests.get(url)
    if wb_data.status_code == 404:
        # 该页面不存在,或该商品已经卖出
        pass
    else:
        soup = BeautifulSoup(wb_data.text,'lxml')
        title = soup.select('h1.info_titile')[0].text if soup.select('h1.info_titile') else None
        lable = list(map(lambda x: x.text,soup.select('div.biaoqian_li > span'))) if soup.select('div.biaoqian_li > span') else None
        price_now = soup.select('span.price_now > i')[0].text if soup.select('span.price_now > i') else None
        price_ori = soup.select('b.price_ori')[0].text if soup.select('b.price_ori') else None
        area = soup.select('div.place_li > i')[0].text if soup.select('div.place_li > i') else None
        data = {
            'title':title,
            'lable':lable,
            'price_now':price_now,
            'price_ori':price_ori,
            'area':area
        }
        commodity_infomation.insert_one(data)
        time.sleep(2)
        print(data)
def test():
    get_commodity_infomation('http://zhuanzhuan.ganji.com/detail/751793048516018180z.shtml')

if __name__ == '__main__':
    test()