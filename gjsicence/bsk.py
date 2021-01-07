# -*- coding: UTF-8 -*- 
import urllib.request, http.client, json, time, datetime
import os
import settings
import django
import sys
import time
import tushare as ts
# 300875
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'gjsicence.settings' 
django.setup()

from server.models import Stock, FinancialStatement, IncomeStatement, BalanceStatement, CashFlowStatement

pro = ts.pro_api(token="c3ebbfac31ace68059c0acae3c76eff6a391d09fa59fd20849fca141")
# stock_list = Stock.objects.all()
# date_list = ["20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]
# for date in date_list:
	# index = 0
	# for stock_index in range(0, 67):
		# print(date)
		# print(index)
		# stock_group = stock_list[index: index+60]
		# if stock_group:
			# stock_str = ""
			# for stock in stock_group:
				# exchange = ".SZ" if stock.exchange == "SZSE" else ".SH"
				# stock_str += (stock.symbol+exchange+',')
			# time.sleep(1)
			# df = pro.fina_indicator(ts_code=stock_str, period=date, fields='ts_code,cash_to_liqdebt,fixed_assets,arturn_days,ocf_to_debt,roa,roic,assets_to_eqt')
			# for data in df.itertuples():
				# code = data[1].split(".")[0]
				# arturn_days = str(data[2])
				# roa = str(data[3])
				# roic = str(data[4])
				# assets_to_eqt = str(data[5])
				# ocf_to_debt = str(data[6])
				# fixed_assets = str(data[7])
				# cash_to_liqdebt = str(data[8])
				
				# financial_list = FinancialStatement.objects.filter(
					# publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
					# stock_code=code
				# )
				# if financial_list:
					# financial_list = financial_list[0]
					# financial_list.arturn_days = arturn_days
					# financial_list.roa = roa
					# financial_list.roic = roic
					# financial_list.assets_to_eqt = assets_to_eqt
					# financial_list.ocf_to_debt = ocf_to_debt
					# financial_list.fixed_assets = fixed_assets
					# financial_list.cash_to_liqdebt = cash_to_liqdebt
					# financial_list.save()
			# index += 60
	
# df = pro.fina_indicator(ts_code='002824,002825,002826,002827,002828,002829,002830,002831,002832,002833,002835,002836,002837,002838,002839,002840,002841,002842,002843,002845,002846,002847,002848,002849,002850,002851,002852,002853,002855,002856,002857,002858,002859,002860,002861,002862,002863,002864,002865,002866,002867,002868,002869,002870,002871,002872,002873,002875,002876,002877,002878,002879,002880,002881,002882,002883,002884,002885,002886,002887,', period='20161231', fields='cash_to_liqdebt,fixed_assets,arturn_days,ocf_to_debt,roa,roic,assets_to_eqt')
# for stock in df.itertuples():
	# print(stock)
date_list = ["20141231", "20151231", "20161231", "20171231", "20181231", "20191231", ]
industry_str = """银行      
全国地产  
互联网    
环境保护  
区域地产  
酒店餐饮  
运输设备  
综合类    
建筑工程  
玻璃      
家用电器  
文教休闲  
其他商业  
元器件    
IT设备    
其他建材  
汽车服务  
火力发电  
医药商业  
汽车配件  
广告包装  
轻工机械  
新型电力  
多元金融  
饲料      
电气设备  
房产服务  
石油加工  
铅锌      
农业综合  
批发业    
通信设备  
旅游景点  
港口      
机场      
石油贸易  
空运      
医疗保健  
商贸代理  
化学制药  
影视音像  
工程机械  
软件服务  
证券      
化纤      
水泥      
生物制药  
专用机械  
供气供热  
农药化肥  
机床制造  
百货      
中成药    
路桥      
造纸      
食品      
黄金      
化工原料  
矿物制品  
水运      
日用化工  
机械基件  
汽车整车  
煤炭开采  
铁路      
染料涂料  
白酒      
林业      
水务      
水力发电  
旅游服务  
纺织      
铝        
保险      
园区开发  
小金属    
铜        
普钢      
航空      
特种钢    
种植业    
出版业    
焦炭加工  
啤酒      
公路      
超市连锁  
钢加工    
渔业      
农用机械  
软饮料    
化工机械  
塑料      
红黄酒    
橡胶      
家居用品  
摩托车    
电器仪表  
服饰      
仓储物流  
纺织机械  
电器连锁  
装修装饰  
半导体    
电信运营  
石油开采  
乳制品    
商品城    
公共交通  
船舶      
NULL      
陶瓷"""
industry_list = industry_str.split("\n")

def add_roic_score(date):

	financial_list = FinancialStatement.objects.filter(
		publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
	)
	for financial in financial_list:
		
		print(financial.stock_code)
		stock_ = financial
		stock_code = financial.stock_code
		stock_data = json.loads(stock_.statement_content)
		current_ratio = stock_data["data"][0][stock_data["columns"].index("current_ratio")]
		quick_ratio = stock_data["data"][0][stock_data["columns"].index("quick_ratio")]
		
		current_ratio = current_ratio if current_ratio else 0
		quick_ratio = quick_ratio if quick_ratio else 0
		
		if current_ratio > 2.5:
			current_ratio_score = 40
		elif current_ratio > 1 and current_ratio <= 2.5:
			current_ratio_score = 20
		elif current_ratio > 0 and current_ratio <= 1:
			current_ratio_score = 10
		else:
			current_ratio_score = 0
			
		if quick_ratio > 1.5:
			quick_ratio_score = 60
		elif quick_ratio > 1 and quick_ratio <= 1.5:
			quick_ratio_score = 40
		elif quick_ratio > 0.5 and quick_ratio <= 1:
			quick_ratio_score = 20
		elif quick_ratio > 0 and quick_ratio <= 0.5:
			quick_ratio_score = 10
		else:
			quick_ratio_score = 0
			
		cash_to_liqdebt =  financial.cash_to_liqdebt
		cash_to_liqdebt = float(cash_to_liqdebt) if cash_to_liqdebt else 0
		if cash_to_liqdebt > 0.25:
			cash_to_liqdebt_score = 50
		elif cash_to_liqdebt > 0.2 and cash_to_liqdebt <= 0.25:
			cash_to_liqdebt_score = 40
		elif cash_to_liqdebt > 0.15 and cash_to_liqdebt <= 0.2:
			cash_to_liqdebt_score = 30
		elif cash_to_liqdebt > 0.1 and cash_to_liqdebt <= 0.15:
			cash_to_liqdebt_score = 20
		elif cash_to_liqdebt > 0.05 and cash_to_liqdebt <= 0.1:
			cash_to_liqdebt_score = 10
		else:
			cash_to_liqdebt_score = 0
			
		ocf_to_debt = financial.ocf_to_debt
		ocf_to_debt = float(ocf_to_debt) if ocf_to_debt else 0
		if ocf_to_debt > 1:
			ocf_to_debt_score = 20
		elif ocf_to_debt <=1 and ocf_to_debt > 0:
			ocf_to_debt_score = 10
		else:
			ocf_to_debt_score = 0
			
		arturn_days = financial.arturn_days
		arturn_days = float(arturn_days) if arturn_days else 180
		if arturn_days < 15:
			arturn_days_score = 30
		elif arturn_days >=15 and arturn_days < 30:
			arturn_days_score = 25
		elif arturn_days >=30 and arturn_days < 60:
			arturn_days_score = 20
		elif arturn_days >=60 and arturn_days < 90:
			arturn_days_score = 15
		elif arturn_days >=90 and arturn_days < 150:
			arturn_days_score = 10
		elif arturn_days >=150 and arturn_days < 180:
			arturn_days_score = 5
		else:
			arturn_days_score = 0
		
		cash_flow_score = ocf_to_debt_score + arturn_days_score + cash_to_liqdebt_score
		dept_paying_score = current_ratio_score + quick_ratio_score
		print(cash_flow_score, dept_paying_score)
		financial.cash_flow_score = cash_flow_score
		financial.dept_paying_score = dept_paying_score
		financial.save()
		
		
		
		
		
	# stock_data_dict = {}
	# for industry in industry_list:
		
		# stock_data_dict[industry] = {}
		# stock_data_list2 = []
		# stock_list = Stock.objects.filter(
			# industry=industry.strip()
		# )
		# print(industry.strip())
		# for stock in stock_list:
			
			# stock_ = FinancialStatement.objects.filter(
				# publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
				# stock_code=stock.symbol
			# )
			
			# if stock_:
				# print(stock_[0].stock_code)
				# stock_ = stock_[0]
				# stock_code = stock_.stock_code
				# stock_data = json.loads(stock_.statement_content)
				# em = stock_data["data"][0][stock_data["columns"].index("assets_to_eqt")]
				# em = em if em else 100
				# stock_data_list2.append([stock_code, em])
		# stock_data_list2.sort(key=lambda x:x[1])
		# num = 1
		# for stock__ in stock_data_list2:
			# stock_data_dict[industry][stock__[0]] = str(100 - (num / len(stock_data_list2) * 100))
			# num += 1
	# print(stock_data_dict)
	
	# for i in stock_data_dict.keys():
		
		# for j in stock_data_dict[i].keys():
			# print(j)
			# stock = FinancialStatement.objects.filter(
				# publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
				# stock_code=j
			# )
			# if stock:
				# stock = stock[0]
				# stock.EM_score = stock_data_dict[i][j]
				# stock.save()
	
	
	
	
	
	
	
	
	
	# stock_score_list = []
	# stock_score_list2 = []
	# for stock in stock_list:
		# stock_data = json.loads(stock.statement_content)
		# roa = stock_data["data"][0][stock_data["columns"].index("roa")]
		# roa = roa if roa else 0
		# roic = stock_data["data"][0][stock_data["columns"].index("roic")]
		# roic = roic if roic else 0
		# stock_code = stock.stock_code
		# stock_score_list.append([stock_code, roa])
		# stock_score_list2.append([stock_code, roic])
	# stock_score_list.sort(key=lambda x:x[1])
	# stock_score_list2.sort(key=lambda x:x[1])
	# stock_dict = {}
	# stock_dict2 = {}
	# num = 1
	# for stock_data in stock_score_list:
		# rank = str((num / len(stock_score_list) * 100))
		# num += 1
		# stock_dict[stock_data[0]] = rank
		
	# num = 1
	# for stock_data2 in stock_score_list2:
		# rank = str((num / len(stock_score_list2) * 100))
		# num += 1
		# stock_dict2[stock_data2[0]] = rank
		
	# flag = 0
	# for stock_f in stock_list:
		# print(flag)
		# flag += 1
		# stock_f.ROA_score = stock_dict[stock_f.stock_code]
		# stock_f.ROIC_score = stock_dict2[stock_f.stock_code]
		# print(stock_dict[stock_f.stock_code], stock_dict2[stock_f.stock_code])
		# stock_f.save()
		
for date in date_list:
	add_roic_score(date)
# def stocklist():

	# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,list_date,delist_date')
	# count = 0
	# for stock in data.itertuples():
		
	
		# count += 1
		# if count > 2254:
			# print(getattr(stock, "symbol"))
			# for date in date_list:
				# time.sleep(1)
				# exchange = ".SZ" if getattr(stock, "symbol") == "SZSE" else ".SH"
				# df = pro.fina_indicator(ts_code=getattr(stock, "symbol")+exchange, period=date)
				# df = pro.fina_indicator(ts_code="300875.SZ", period=date)
				# if df.empty:
					# pass
				# else:
					# json_data = df.to_json(orient = 'split', force_ascii = False)
					# FinancialStatement.objects.create(
						# stock_code = getattr(stock, "symbol"),
						# stock_code = "300875",
						# exchange = getattr(stock, "exchange"),
						# exchange = "SZSE",
						# publish_date = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
						# statement_content = json_data
					# )
			
		
		# exchange = getattr(stock, "exchange")
		# symbol = getattr(stock, "symbol")
		# name_cn = getattr(stock, "name")
		# name_en = getattr(stock, "enname")
		# name_full = getattr(stock, "fullname")
		# area = getattr(stock, "area")
		# industry = getattr(stock, "industry")
		# market = getattr(stock, "market")
		# list_status = getattr(stock, "list_status")
		# list_date = getattr(stock, "list_date")
		# delist_date = getattr(stock, "delist_date")
		
		# Stock.objects.create(
			# exchange=exchange, 
			# symbol=symbol,
			# name_cn=name_cn,
			# name_en=name_en,
			# name_full=name_full,
			# area=area,
			# industry=industry,
			# market=market,
			# list_status=list_status,
			# list_date=list_date,
			# delist_date=delist_date
		# )

# stocklist()

