import pymongo
import os
import settings
import django
import sys
import json
import download_from_tushare
import time
import pymysql

client = pymongo.MongoClient("mongodb://localhost:27017/")
indexdb = client["index"]
targetdb = client["resultdb"]
connect = pymysql.connect(
	host = "localhost",
	user = "root",
	password = "123456",
	database = "gjscience",	
)
cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

date_list = ["20131231", "20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]

for date in date_list:
	stock_year_list = []
	industry_dict = {} 
	for stock in targetdb.list_collection_names():
		col_set = list(targetdb[stock].find({"publish_date": date}))
		# targetdb[stock].delete_one({"stock_code": stock})
		print(len(col_set))		
		if len(col_set) == 1:
		
			roa = indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F016N"]
			roa = roa if roa else 0
			roe = indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F014N"]
			roe = roe if roe else 0
			em = indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F118N"] / indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F128N"]
			em = em if em else 0
			
			sql = "SELECT industry FROM server_stock WHERE symbol = %s" % stock
			cursor.execute(sql)
			industry = cursor.fetchall()[0]["industry"]
			
			try:
				if industry_dict[industry]:
					industry_dict[industry].append((stock, em))
			except KeyError:
				industry_dict[industry] = [(stock, em)]
			
			pay = 0
			current_ratio = indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F042N"]
			quick_ratio = indexdb[stock].find({"ENDDATE": date[0:4]+"-"+date[4:6]+"-"+date[6:]})[0]["F043N"]
			if current_ratio >= 2.5:
				pay += 40
			elif current_ratio >= 1 and current_ratio < 2.5:
				pay += 20
			elif current_ratio >= 0 and current_ratio < 1:
				pay += 10
			else:
				pay += 0
				
			if quick_ratio >= 1.5:
				pay += 60
			elif quick_ratio >= 1 and quick_ratio < 1.5:
				pay += 40
			elif quick_ratio >= 0.5 and quick_ratio < 1:
				pay += 20
			elif quick_ratio >= 0 and quick_ratio < 0.5:
				pay += 10
			else:
				pay += 0
			
			cash = 0
			if col_set[0]["cash_to_assets_ratio"] >= 0.25:
				cash += 50
			elif col_set[0]["cash_to_assets_ratio"] >= 0.2 and col_set[0]["cash_to_assets_ratio"] < 0.25:
				cash += 40
			elif col_set[0]["cash_to_assets_ratio"] >= 0.15 and col_set[0]["cash_to_assets_ratio"] < 0.2:
				cash += 30
			elif col_set[0]["cash_to_assets_ratio"] >= 0.1 and col_set[0]["cash_to_assets_ratio"] < 0.15:
				cash += 20
			elif col_set[0]["cash_to_assets_ratio"] >= 0.05 and col_set[0]["cash_to_assets_ratio"] < 0.1:
				cash += 10
			elif col_set[0]["cash_to_assets_ratio"] >= 0 and col_set[0]["cash_to_assets_ratio"] < 0.05:
				cash += 5
			else:
				cash += 0
				
			try:
				if col_set[0]["operation_cash_flow_ratio"] > 1 and col_set[0]["cash_adequancy_ratio"] > 1 and col_set[0]["crir"] > 0.1:
					cash += 20
				elif col_set[0]["operation_cash_flow_ratio"] < 0 and col_set[0]["cash_adequancy_ratio"] < 0 and col_set[0]["crir"] < 0:
					cash += 0
				else:
					cash += 10
			except TypeError:
				cash += 10
				
			try:
				if col_set[0]["accounts_receiv_turnover"] <= 15:
					cash += 30
				elif col_set[0]["accounts_receiv_turnover"] <= 30 and col_set[0]["accounts_receiv_turnover"] > 15:
					cash += 25
				elif col_set[0]["accounts_receiv_turnover"] <= 60 and col_set[0]["accounts_receiv_turnover"] > 30:
					cash += 20
				elif col_set[0]["accounts_receiv_turnover"] <= 90 and col_set[0]["accounts_receiv_turnover"] > 60:
					cash += 16
				elif col_set[0]["accounts_receiv_turnover"] <= 150 and col_set[0]["accounts_receiv_turnover"] > 90:
					cash += 12
				elif col_set[0]["accounts_receiv_turnover"] <= 180 and col_set[0]["accounts_receiv_turnover"] > 150:
					cash += 8
				else:
					cash += 4
			except TypeError:
				cash += 16
				
			targetdb[stock].update_one({"publish_date": date}, {"$set": {"pay_score": pay, "cash_score": cash}})
			stock_year_list.append((stock, roa, roe))
	stock_year_list.sort(key=lambda x: float(x[1]))
	for stock_item in stock_year_list:
		roa = stock_year_list.index(stock_item) / len(stock_year_list) * 100
		targetdb[stock_item[0]].update_one({"publish_date": date}, {"$set": {"roa_score": roa}})
	stock_year_list.sort(key=lambda x: float(x[2]))
	for stock_item in stock_year_list:
		roe = stock_year_list.index(stock_item) / len(stock_year_list) * 100
		targetdb[stock_item[0]].update_one({"publish_date": date}, {"$set": {"roe_score": roe}})
			
		
	for k, v in industry_dict.items():
		v.sort(key=lambda x: x[1], reverse=True)
		for em_item in v:
			em_score = v.index(em_item) / len(v) * 50 + 50
			targetdb[em_item[0]].update_one({"publish_date": date}, {"$set": {"em_score": em_score}})
				
			
			
	print(industry_dict)
	