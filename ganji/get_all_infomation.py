#! -*-encoding:utf-8-*-
'''
该模块功能：获取该网站所有二手商品的详细信息
'''

from save_commodity_url import commodity_urls
from multiprocessing import Pool
from get_commodity_infomation import get_commodity_infomation

def get_all_commodity_info():
    '''获取所有的商品信息'''

    commodity_links = [item['url'] for item in commodity_urls.find()]
    print(commodity_links)
    pool = Pool()
    pool.map(get_commodity_infomation,commodity_links)

def test():
    get_all_commodity_info()

if __name__ == '__main__':
    test()