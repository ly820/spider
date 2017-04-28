#!/usr/bin/env python3.5
#-*- encoding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
import time


#url = 'http://bj.xiaozhu.com/fangzi/5956869116.html'
def get_house_info(url):
    '''
    传入房源的url，以列表的形式返回房子及房主的信息。
    '''
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    #print(soup)
    title = soup.select('div.pho_info > h4 > em')[0].get_text()
    address = soup.select('div.pho_info > p')[0].get('title')
    price_per_day =''.join(soup.select('div.day_l')[0].stripped_strings)
    image = soup.select('#detailImageBox > div.pho_show_r > div > ul > li:nth-of-type(2) > img')[0].get('data-src')
    house_ower_img = soup.select('div.member_pic > a > img')[0].get('src')
    sex = '男' if soup.select('div.member_ico') else '女'
    #if soup.select('div.member_ico'):
    #    sex = '男'
    #else:
    #    sex = '女'
    house_ower_name = soup.select('.lorder_name')[0].get_text()
    return [title,address,price_per_day,image,house_ower_img,sex,house_ower_name]

#a = get_house_info(url)
#print(a)

def get_house_url(num=10):
    '''
    @ num: 你想获得的页数
    返回10页所有的房源的地址
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

wb = Workbook()
table = wb.active
table.title = '小猪短租房信息'
header = ['标题','地址','日租金','房源首图片链接','房东图片链接','房东性别','房东名字']
table.append(header)
i = 1
urls = get_house_url()
for url in urls:
    print('正在保存第%s个房源信息'%i)
    #time.sleep(2)
    info = get_house_info(url)
    table.append(info)
    i += 1

wb.save('/home/liuyuan/桌面/python_code/小猪短租房/小猪短租房信息.xls')
print('保存完毕，请在桌面查看')    

