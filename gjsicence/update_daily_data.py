import urllib.request, http.client, json, time, datetime
import datetime
import pymongo
import time
import tushare as ts

client = pymongo.MongoClient("mongodb://localhost:27017/")
daylinedb = client["daylinedb"]
collist = daylinedb.list_collection_names()
date_list = ["20201107", "20201108", "20201109", "20201110", "20201111", "20201112", "20201113", "20201114", "20201115", "20201116", "20201117", "20201118", "20201119", "20201120", "20201121", "20201122", "20201123", "20201124", "20201125", "20201126", "20201127", "20201128", "20201129", "20201130", ]
pro = ts.pro_api(token="df36b05825c5f945cdd1b566f85f69d6db45e597765a0bdc9f616f44")
start_date = (datetime.datetime.now()+datetime.timedelta(days=-365)).strftime("%Y%m%d")
# end_date = datetime.datetime.now().strftime("%Y%m%d")
# daily_data = pro.daily(trade_date=datetime.datetime.now().strftime("%Y%m%d"))
for end_date in date_list:
	daily_data = pro.daily(trade_date=end_date).to_dict(orient='records')
	time.sleep(1)
	# index_data = pro.index_daily(ts_code='000300.Sh', start_date=start_date, end_date=end_date).to_dict(orient='records')
	if daily_data:
		for stock in daily_data:
			print(stock)
			stock_dict = {
				"symbol": stock["ts_code"][0:6],
				"exchange": stock["ts_code"][7:].lower(),
				"date": stock["trade_date"],
				"open": stock["open"],
				"close": stock["close"],
				"high": stock["high"],
				"low": stock["low"],
				"pre_close": stock["pre_close"],
				"change": stock["change"],
				"chg": stock["pct_chg"],
				"volume": stock["vol"],
				"amount": stock["amount"],
			}
			daylinedb[stock["ts_code"][0:6]].insert_one(stock_dict)
# print(index_data)	
# for stock in collist:
	# if stock == "000651":
		# query = {
			# "date": {
				# "$gte": start_date,
			# }
		# }
		# data_list = list(daylinedb[stock].find(query))
		# index_data = index_data[-(len(data_list)+1): -1]
		# for l in list(data_list):
			# print(index_data[list(data_list).index(l)])

	