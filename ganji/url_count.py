from save_commodity_url import commodity_urls
import time

while True:
    print(commodity_urls.find().count())
    time.sleep(3)