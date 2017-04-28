#!/usr/bin/env python3
#-*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import time

#url = 'http://jandan.net/ooxx/page-2262'

def get_image(url):
    '''传入url,获得该页面图片,并建立相应的目录,存储图片'''
    headers = {
        'Host': 'jandan.net',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    }

    # 根据传入的url,建立相应的目录
    print('正在新建目录')
    name = url.split('/')[-1]
    os.mkdir('/home/liuyuan/桌面/python_code/煎蛋网妹子图片/'+name)
    #print(directory)
    # 获得页面图片链接
    wb_data = requests.get(url,headers=headers)
    if not wb_data.status_code == 200:
        print('请求失败,请重新尝试')
        return None
    soup = BeautifulSoup(wb_data.text,'lxml')
    images = soup.select('div.text > p > img[src$=".jpg"]')
    number = len(images)
    print('该页一共有{}张图片'.format(number))
    # 遍历所有图片链接,请求,获得图片的二进制,保存到图片文件中
    for index,image in enumerate(images):
        time.sleep(1)
        print('正在保存第{}张图片'.format(index))
        img = requests.get(image['src']).content
        path = '/home/liuyuan/桌面/python_code/煎蛋网妹子图片/' + name +'/{}.jpg'.format(index)
        with open(path,'wb') as f:
            f.write(img)

#get_image(url)
def getpage():
    '''获得指定页的图片'''
    num =  input('请输入页数：')
    url = 'http://jandan.net/ooxx/page-{}'.format(num)
    get_image(url)

def getpages():
    '''获得指定页码范围内所有页面的图片'''
    # 起始页码
    start = int(input('请输入起始页码：'))
    # 结束页码
    end = int(input('请输入结束页码：')) + 1
    # 生成页码对应的url链接
    urls = ['http://jandan.net/ooxx/page-{}'.format(str(i)) for i in range(start,end)]
    for url in urls:
        time.sleep(2)
        get_image(url)

if __name__=='__main__':
    # 程序开始时间
    print(time.time())
    print('方式1：输入1,获得指定页码的图片')
    print('方式2：输入2,获得制定页码范围内的图片')
    i = input('请输入你选择的方式：')
    if i == '1':
        getpage()
        print('完成任务！请您查看')
        print(time.time())
    elif i == '2':
        getpages()
        print('完成任务！请您查看')
        print(time.time())
    else:
        print('对不起您输入有误！')
        print(time.time())