#! -*-encoding:utf-8-*-
'''
该模块功能：获取该网站所有二手商品的url链接
'''

from channel_extract import get_channel_urls
from save_commodity_url import get_all_commodity_links
from multiprocessing import Pool


def get_all_links():
    # 获取改网站所有二手商品的详情url
    url = 'http://bj.ganji.com/wu'
    channel_list = get_channel_urls(url)
    pool = Pool()
    pool.map(get_all_commodity_links, channel_list)
    print('以为您保存完所有商品链接,请注意查收.')

def test():
    get_all_links()

if __name__ == "__main__":
    test()

