#! -*-encoding:utf-8-*-
'''
该模块的功能：保存给定频道到所有商品详情网页链接。
'''


from bs4 import BeautifulSoup
import requests
import pymongo
import time
#设置代理与要用
#import random

# 链接数据库,创建数据库ganji,并建立数据表保存所有的商品url链接
client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
commodity_urls = ganji['commodity_urls']  # 保存商品链接的数据表

# 设置头部信息
headers = {
        'Host':'bj.ganji.com',
        'Referer':'http://bj.ganji.com/wu/',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    }

# 设置代理IP
#proxy_list = [
#    'http://101.251.199.66:3128',
#    'http://101.200.40.179:8118',
#    'http://123.117.86.89:9000'
#]
#proxy_ip = random.choice(proxy_list)
#proxies = {'http':proxy_ip}
# 如果设置了代理IP,requests.get(url,headers=headers,proxies=proxies)

def get_commodity_url(channel,page):

    '''提取频道分类中给定页数的商品url链接'''

    # 根据传入的channel,page等信息构造url链接
    url = '{}o{}'.format(channel,str(page)) # 该链接类似 http://bj.ganji.com/jiaju/o2/
    try:
        wb_data = requests.get(url,headers=headers)
    except (requests.HTTPError,requests.ConnectionError) as e:
        print('链接不成功。')
        print('该网页url是：',url)
        pass
    else:
        soup = BeautifulSoup(wb_data.text,'lxml')
        # 判断该页面是否有商品信息
        if soup.select('.noinfo'):
            # 该页面没有所需信息
            pass
        else:
            # 判断能否找到所需元素
            links = soup.select('td.img  > a') if soup.select('td.img  > a') else None
            if links:
                for link in links:
                    #print(link.get('href').split('?')[0])
                    # 去除url链接中多余的信息,并存入数据库中
                    data = {
                        'url':link.get('href').split('?')[0]
                    }
                    print(data)
                    commodity_urls.insert_one(data)
            else:
                print('该页面没有所需元素,可能网页源代码,发生变化,尝试修改程序解决问题')
                pass
        time.sleep(2)

def get_all_commodity_links(channel):

    '''获取所给频道所有商品链接'''
    for num in range(1,101):
        get_commodity_url(channel,num)

def test():
    get_commodity_url('http://bj.ganji.com/jiaju/',2)

if __name__ == '__main':
    test()
