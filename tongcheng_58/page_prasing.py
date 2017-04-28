from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info']

# spider 1
def get_links_from(channel,pages):
    list_view = '{}pn{}'.format(channel,str(pages))

    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')

    if soup.find('td','t'):
        for link in soup.select('tr.zzinfo > td.t > a'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url':item_link})
            print(item_link)
    else:
        pass
    time.sleep(2)

# spider2
def get_item_info(url):

    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    no_exitstance = soup.find('script',type='text/javascript').get('src')
    if no_exitstance:
        if '404' in no_exitstance.strip('/'):
            pass
    else:
        title = soup.select('h1.info_titile')[0].text if soup.select('h1.info_titile') else None
        price = soup.select('span.price_now > i')[0].text if soup.select('span.price_now > i') else None
        label = list(soup.select('div.biaoqian_li')[0].stripped_strings) if soup.select('div.biaoqian_li') else None
        seller = soup.select('p.personal_name')[0].text if soup.select('p.personal_name') else None
        views = soup.select('span.look_time')[0].text if soup.select('span.look_time') else None
        img_treasure = [img['src'] for img in soup.select('div.boby_pic > img')] if soup.select('div.boby_pic > img') else None
        area = soup.select('div.palce_li i')[0].text if soup.select('div.palce_li i') else None

        data = {
            'title':title,
            'price':price,
            'label':label,
            'area':area,
            'seller':seller,
            'views':views,
            'img_treasure':img_treasure
        }
        print(data)
        item_info.insert_one(data)
    #time.sleep()

#get_item_info('http://zhuanzhuan.58.com/detail/805090286639300615z.shtml')
