import pymongo
import os
import settings
import django
import sys
import json
import download_from_tushare
import time

client = pymongo.MongoClient("mongodb://localhost:27017/")
indexdb = client["index"]
targetdb = client["resultdb"]

date_list = ["20131231", "20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]



for stock in indexdb.list_collection_names():
	
	doc_set = list(indexdb[stock].find())
	# if len(doc_set) != 7:
		# print(stock)
		# print(len(doc_set))
	print(stock)
	target_col = targetdb[stock]
	sigh = 0
	for index_data in doc_set:
		
		try:
			index_data["type"]
			# print(index_data["type"])
		except KeyError:
			stock_code = stock
			publish_date = index_data["ENDDATE"].replace("-", "")
			cash_to_assets_ratio = index_data["F044N"] # 现金比率
			operation_cash_flow_ratio = index_data["F105N"] / index_data["F119N"] # 现金流量比率 = 经营现金流量净额 / 流动负债
			crir = index_data["F105N"] / (index_data["F118N"] - index_data["F119N"]) # 现金再投资比率 = 经营现金流量净额 / (总资产 - 流动负债)
			accounts_receiv_turnover = index_data["F027N"] # 应收账款周转天数
			gross_profit_margin = index_data["F078N"] # 毛利率
			cost_rate = index_data["F079N"] # 费用率
			income_rate = index_data["F017N"] # 净利率
			roe = index_data["F081N"] # 净资产收益率
			basic_eps = index_data["F004N"] # 基本每股收益
			total_assets_turnover = index_data["F025N"] # 总资产周转率
			inventories_turnover = index_data["F028N"] # 存货周转天数
			try:
				business_days = inventories_turnover + accounts_receiv_turnover # 完整生意周期 = 存货周转天数 + 应收账款周转天数
			except TypeError:
				business_days = None
			kmpr = index_data["F080N"] # 缺钱天数 (现金转换周期)
			debt_to_assets_ratio = index_data["F041N"] # 资产负债比率
			try:
				longterm_assets_to_fix_assets_ratio = (index_data["F120N"] + index_data["F128N"]) / (index_data["F116N"]) # 长期资金占不动产及设备比率 = (非流动性负债 + 股东权益) / (固定资产)
			except TypeError:
				longterm_assets_to_fix_assets_ratio = None
			quick_ratio = index_data["F043N"] # 速动比率
			if sigh >= 2:
				try:
					cash_adequancy_ratio = (doc_set[sigh-2]["F105N"] + doc_set[sigh-1]["F105N"] + doc_set[sigh]["F105N"]) / ((doc_set[sigh-2]["F106N"] + doc_set[sigh-1]["F106N"] + doc_set[sigh]["F106N"]) + (doc_set[sigh-2]["F107N"] + doc_set[sigh-1]["F107N"] + doc_set[sigh]["F107N"]) + (doc_set[sigh]["F112N"] - doc_set[sigh-2]["F112N"]))
				except TypeError:
					cash_adequancy_ratio = None
					
				try:
					operation_growth_ratio = (doc_set[sigh]["F052N"] + doc_set[sigh-1]["F052N"] + doc_set[sigh-2]["F052N"]) / 3
				except TypeError:
					operation_growth_ratio = None
			else:
				cash_adequancy_ratio = None
				operation_growth_ratio = None
			sigh += 1
			
			data_dict = {
				"stock_code": stock_code,
				"publish_date": publish_date,
				"cash_to_assets_ratio": cash_to_assets_ratio,
				"operation_cash_flow_ratio": operation_cash_flow_ratio,
				"crir": crir,
				"accounts_receiv_turnover": accounts_receiv_turnover,
				"gross_profit_margin": gross_profit_margin,
				"cost_rate": cost_rate,
				"income_rate": income_rate,
				"roe": roe,
				"basic_eps": basic_eps,
				"total_assets_turnover": total_assets_turnover,
				"inventories_turnover": inventories_turnover,
				"business_days": business_days,
				"kmpr": kmpr,
				"debt_to_assets_ratio": debt_to_assets_ratio,
				"longterm_assets_to_fix_assets_ratio": longterm_assets_to_fix_assets_ratio,
				"quick_ratio": quick_ratio,
				"cash_adequancy_ratio": cash_adequancy_ratio,
				"operation_growth_ratio": operation_growth_ratio
			}
			
			target_col.update_one(data_dict, {'$set': data_dict})
				
				
				
				
				
				