import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import os
from hashlib import md5
from json import JSONDecodeError
import re
import pymongo
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
tb = db[MONGO_TB]


def get_page_index(offset,keyword,cur_tab='3'):
    """

    :param offset: 构造请求的页面的页码信息,offset 为0,20,40等等,
    :param keyword:请求的关键字,如：'街拍'
    :param cur_tab:请求图集相关信息
    :return:返回页面源代码
    """
    # 构造url所需的参数
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab':cur_tab
    }
    # 构造url
    url = "http://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if  response.status_code == 200:
            return response.text
        else:
            print("没有更多的数据了")
    except RequestException:
        print("索引页请求出错",url)
        return None


def parse_page_index(html):
    """

    :param html: 索引页的源码
    :return: 返回一个url的生成器
    """
    try:
        # 页面源码是json格式的,这里的html是字符串,需要将其转换成json格式
        items = json.loads(html)
        if items and 'data' in items.keys():
            #print(len(items['data']))
            for item in items['data']:
                url = item['url']
                #url_list = get_page_details(url)
                yield url
    # 可能出现的错误
    except JSONDecodeError:
        pass



def parse_page_details(url):
    """

    :param url: 详情页的url
    :return: 返回一个生成器(包含该页面的title,image信息)
    """
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        title = soup.select('head > title')[0].get_text() if soup.select('head > title') else None
        print(title)
        # 因为页面中的图片是javascript动态加载的,所以用正则表达式
        pattern = re.compile(r'var gallery = (.*?);',re.S)
        result = re.search(pattern,html.text)
        if result:
            try:
                # group(1) 在页面中其实是一个字典,但此刻它是一个字符串,需要装换成json格式
                data = json.loads(result.group(1))
                if data and 'sub_images' in data.keys():
                    sub_images = data.get('sub_images')
                    images = [item.get('url') for item in sub_images]
                    for image in images:
                        # 下载图片至程序所在文件夹下
                        download_images(image)
                    yield {
                        'title':title,
                        'images':images
                    }
            except JSONDecodeError:
                pass
    except RequestException:
        print("请求详情页出错",url)
        return None




def download_images(url):
    """

    :param url: 加载图片的url
    :return:
    """
    print("正在下载图片：",url)
    try:
        html = requests.get(url)
        content = html.content
        path = '{0}/{1}.jpg'.format(os.getcwd(),md5(content).hexdigest())
        save_to_file(path,content)
        return None

    except RequestException:
        print("请求图片失败",url)
        return None

def save_to_file(path,content):
    """

    :param path: 保存图片的路径
    :param content: 图片的二进制字节流
    :return: None
    """
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(content)
        return None

def main(offset):
    html = get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        for data in parse_page_details(url):
            print(data)
            if tb.insert_one(data):
                print("保存至数据库成功")
            else:
                print("保存至数据库失败")



if __name__ == "__main__":
    offsets = [i*20 for i in range(OFFSET_START,OFFSET_END+1)]
    pool = Pool()
    pool.map(main,offsets)
