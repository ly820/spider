
from page_prasing import get_item_info
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']

urls = (item['url'] for item in url_list.find())
if __name__ == '__main__':
    pool = Pool()
    pool.map(get_item_info,list(urls))
