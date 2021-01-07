import pymongo
import tushare as ts
import time
from functools import reduce
from functools import partial
client = pymongo.MongoClient("mongodb://localhost:27017/")
daylinedb = client["daylinedb"]
# collist = daylinedb.list_collection_names()
stock_list = ["000858", "000651", "600519"]
pro = ts.pro_api(token="df36b05825c5f945cdd1b566f85f69d6db45e597765a0bdc9f616f44")
start_date = '20200101'
end_date = '20201201'
index_data = pro.index_daily(ts_code='000300.SH', start_date=start_date, end_date=end_date).to_dict(orient='records')
index_data.reverse()

def calc_beta(stock_code, start_date, index_data):
	data = list(daylinedb[stock_code].find({"date": {"$gt": start_date}}))
	index_data = index_data[0: len(data)]
	flag = 0
	index_sum = 0
	for index in index_data:
		index_sum += index["pct_chg"]

	data_sum = 0
	for daily in data:
		data_sum += daily["chg"]
	# data_sum = reduce(add_data, data)
	index_ave = index_sum / len(index_data)
	# index_var = reduce(partial(variance, index_ave=index_ave), index_data)
	index_var = 0
	for daily in index_data:
		index_var += (daily["pct_chg"] - index_ave) * (daily["pct_chg"] - index_ave)
	index_var = index_var / len(index_data)	
	E_index = index_ave
	E_data = data_sum / len(data)
	relation_sum = 0
	flag = 0
	for daily in data:
		relation_sum += (daily["chg"] - E_data) * (index_data[flag]["pct_chg"] - E_index)
		flag += 1
	# print(relation_sum / flag, E_data, E_index)
	E_relation = relation_sum / flag
	cov_relation = E_relation
	# for daily in list(data):
		# index_sum += index_data[flag]["pct_chg"]
	beta = cov_relation / index_var
			
	print(stock_code, round(beta, 4))
	
for stock_code in stock_list:
	calc_beta(stock_code, start_date, index_data)