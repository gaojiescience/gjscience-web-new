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

from server.models import Stock, FinancialStatement, IncomeStatement, BalanceStatement, CashFlowStatement, FinancialAnalytical
date_list = ["20151231", "20161231", "20171231", "20181231", "20191231", ]
stock_list = Stock.objects.all()

for stock in stock_list:
	for date in date_list:
		print(date)
		symbol = stock.symbol
		print(symbol)

		balance_statement = BalanceStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		cash_statement = CashFlowStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		if balance_statement and cash_statement:
			try:
				balance_statement = balance_statement[0]
				cash_statement = cash_statement[0]
				balance_data = json.loads(json.loads(balance_statement.statement_content))
				cash_data = json.loads(json.loads(cash_statement.statement_content))
				
				n_cashflow_act = cash_data["n_cashflow_act"]["0"] if cash_data["n_cashflow_act"]["0"] else 0
				total_cur_liab = balance_data["total_cur_liab"]["0"] if balance_data["total_cur_liab"]["0"] else 0
				operation_cash_flow_ratio = n_cashflow_act / total_cur_liab
				target = FinancialAnalytical.objects.filter(
					stock_code=symbol,
					publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
				)
				print(operation_cash_flow_ratio)
				if target.exists():
					target = target[0]
					target.operation_cash_flow_ratio = str(operation_cash_flow_ratio)
					target.save()
			except ZeroDivisionError:
				pass
			except KeyError:
				pass
				
				