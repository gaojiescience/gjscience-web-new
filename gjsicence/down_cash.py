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

from server.models import Stock, FinancialStatement, IncomeStatement, CashFlowStatement

pro = ts.pro_api(token="c3ebbfac31ace68059c0acae3c76eff6a391d09fa59fd20849fca141")
stock_list = Stock.objects.all()
date_list = ["20161231", ]
for date in date_list:
	print(date)
	for stock in stock_list:
		exchange = ".SZ" if stock.exchange == "SZSE" else ".SH"
		time.sleep(1.2)
		df = pro.cashflow(ts_code=stock.symbol+exchange, period=date)
		CashFlowStatement.objects.create(
			stock_code=stock.symbol,
			exchange=stock.exchange,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
			statement_content=json.dumps(df.to_json())
		)