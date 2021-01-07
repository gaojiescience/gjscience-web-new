# -*- coding: UTF-8 -*- 
import requests
import pymongo
import json
import os
import settings
import django
import sys
import time
import execjs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'gjsicence.settings' 
django.setup()

from server.models import Stock
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["index"]

date_list = ["20131231", "20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]
stock_list = Stock.objects.all()

# proxies = {
	# "http": "http://61.135.185.78:80"
# }

is_stop = False
for stock in stock_list:
	symbol = stock.symbol
	collist = mydb.list_collection_names()
	if (symbol) not in collist:
		mycol = mydb[symbol]
		print(symbol)
		for date in date_list:		
			data = {
				"scode": symbol,
				"rdate": date,
				"type": "071001"
			}
		
		
			print(date)
			
			headers = {
				"Accept": "application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding": "gzip, deflate",
				"Accept-Language": "zh-CN,zh;q=0.9",
				"Cache-Control": "no-cache",
				"Connection": "keep-alive",
				"Content-Length": "0",
				"Cookie": "Hm_lvt_c15f89639ef44e119d7e9267a7359d96=1597817777; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1603161404; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b=1603163136",
				"Host": "webapi.cninfo.com.cn",
				"mcode": execjs.compile(open(r"mcode.js").read()).call('indexcode'),
				"Origin": "http://webapi.cninfo.com.cn",
				"Pragma": "no-cache",
				"Referer": "http://webapi.cninfo.com.cn/",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
				"X-Requested-With": "XMLHttpRequest"
			}
			url = "http://webapi.cninfo.com.cn/api/stock/p_stock2303?scode=" + symbol + "&rdate=" + date + "&type=071001"
			json_data = json.loads(requests.post(url, data=data, headers=headers).text)
			print(json_data["resultcode"])
			if json_data["resultcode"] == 200:
				try:
					mycol.update_one(json_data["records"][0], {'$set': json_data["records"][0]}, upsert=True)
				except IndexError:
					continue
				time.sleep(1)
			else:
				is_stop = True
				break
	else:
		continue
	if is_stop:
		break