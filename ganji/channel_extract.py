#! -*-encoding:utf-8-*-
'''
该模块的功能：获取所有频道链接的地址
'''

from bs4 import BeautifulSoup
import requests

def get_channel_urls(url):
    '''获得所有频道的url链接'''
    try:
        wb_data = requests.get(url)
    except (requests.HTTPError,requests.ConnectionError) as e:
        print('链接不成功。')
        print('该网页url是：', url)
        pass
    else:
        soup = BeautifulSoup(wb_data.text,'lxml')
        links = soup.select('dl.fenlei > dt > a') if soup.select('dl.fenlei > dt > a') else None
        if links:
            channel_list = ['http://bj.ganji.com' + link.get('href') for link in links]
            return channel_list
        else:
            print('该网站源码已经修改，请修改程序代码。')

def test():
    url = 'http://bj.ganji.com/wu'
    channel_list = get_channel_urls(url)
    print(channel_list)


if __name__ == '__main__':
    test()
