import pymongo
import requests
client = pymongo.MongoClient("mongodb://localhost:27017/")
indexdb = client["resultdb"]
date_list = ["20131231", "20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]
# proxies = {
	# "http": "http://61.135.185.78:80"
# }

# http = requests.get("https://www.baidu.com/", proxies=proxies).text
# print(http)
# for stock in indexdb.list_collection_names():
	# for date in date_list:
		# col = indexdb[stock].find({"publish_date": date})
		# col_list = list(col)
		# if len(col_list) == 2:
			# indexdb[stock].delete_one({"publish_date": date})
col = list(indexdb["000651"].find())

for doc in col:
		print(doc["publish_date"])
		print(doc["operation_growth_ratio"])
print(len(col))