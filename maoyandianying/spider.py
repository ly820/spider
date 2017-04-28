import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

"""
本程序的功能是爬取猫眼电影TOP100榜单的电影信息,并保存到文件中
"""

def get_one_page(url):
    """

    :param url: 你想要爬取的网址url
    :return: 返回该页面的源代码
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """

    :param html: 需要解析的网页源代码
    :return: 返回一个生成器
    """
    # 提取信息的正则表达式,依次拿到电影的名次,图片,名字,主演,上映时间,评分
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a'
                        +'.*?title="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>'
                        +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:],
            'release_time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    """

    :param content: content是一个字典
    :return: None
    将爬取到的一条信息序列化然后存储到一个文件中(以追加的方式)
    """
    # a 代表一、以追加的方式
    # 为了使保存到文件中的内容正常显示中文,设置encoding参数为'utf-8'，并在序列化时
    # 设置ensure_ascii 为 False
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    """
    打印爬到的信息,并保存到文件中
    """
    #
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == "__main__":
    # 定义一个进程池,以多进程的方式爬取信息
    pool = Pool()
    pool.map(main,[i for i in range(10)])


"""
'<dd>.*?board-index.*?>1</i>.*?data-src="(.*?)".*?name"><a'
+'.*?title="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>'
+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'
"""