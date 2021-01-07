# -*- coding: UTF-8 -*- 
import urllib.request, http.client, json, time, datetime
import os
import settings
import django
import sys
import time
import tushare as ts
from dateutil.relativedelta import relativedelta
# 300875
# CJMZQXCYQMHPKLNP
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'gjsicence.settings' 
django.setup()

from server.models import Stock, FinancialStatement, IncomeStatement, BalanceStatement, CashFlowStatement, FinancialAnalytical
target_date_list = ["20151231", "20161231", "20171231", "20181231", "20191231",]
date_list = ["20111231","20121231","20131231","20141231","20151231", "20161231", "20171231", "20181231", "20191231", ]
stock_list = Stock.objects.all()

for stock in stock_list:
	print(stock.symbol)
	symbol = stock.symbol
	# symbol = "002567"
	res = FinancialAnalytical.objects.filter(
		stock_code=symbol,
		# publish_date=datetime.datetime(int(target[0:4]), int(target[4:6]), int(target[6:8]))
	)
	if res.exists():
		ana_data = CashFlowStatement.objects.filter(
			stock_code=symbol,
			# publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)
		for r in res:
			pub_date = r.publish_date
			print(pub_date)
			sum_act = 0
			sum_pay = 0
			inventories_start = 0
			inventories_end = 0
			for i in range(0, 5):
				cash_statement = CashFlowStatement.objects.filter(
					stock_code=symbol,
					publish_date=pub_date - relativedelta(years=i)
				)
				
				cash_statement = cash_statement[0]
				cash_data = json.loads(json.loads(cash_statement.statement_content))
				try:
					n_cashflow_act = cash_data["n_cashflow_act"]["0"] if cash_data["n_cashflow_act"]["0"] else 0
					c_pay_acq_const_fiolta = cash_data["c_pay_acq_const_fiolta"]["0"] if cash_data["c_pay_acq_const_fiolta"]["0"] else 0
					n_recp_disp_fiolta = cash_data["n_recp_disp_fiolta"]["0"] if cash_data["n_recp_disp_fiolta"]["0"] else 0
					if i == 0:
						balance_statement = BalanceStatement.objects.filter(
							stock_code=symbol,
							publish_date=pub_date - relativedelta(years=i)
						)
						if balance_statement:
							inventories_end = json.loads(json.loads(balance_statement[0].statement_content))["inventories"]["0"]
							inventories_end = inventories_end if inventories_end else 0
					if i == 4:
						balance_statement = BalanceStatement.objects.filter(
							stock_code=symbol,
							publish_date=pub_date - relativedelta(years=i)
						)
						if balance_statement:
							inventories_start = json.loads(json.loads(balance_statement[0].statement_content))["inventories"]["0"]
							inventories_start = inventories_start if inventories_start else 0
					# decr_inventories = cash_data["decr_inventories"]["0"]
					c_pay_dist_dpcp_int_exp = cash_data["c_pay_dist_dpcp_int_exp"]["0"] if cash_data["c_pay_dist_dpcp_int_exp"]["0"] else 0
					sum_act += (n_cashflow_act)
					sum_pay += (c_pay_acq_const_fiolta - n_recp_disp_fiolta + c_pay_dist_dpcp_int_exp)	
				except KeyError:
					continue
			score_data = FinancialStatement.objects.filter(
				stock_code=symbol,
				publish_date=pub_date
			)
			
			score_data = FinancialStatement.objects.filter(
				stock_code=symbol,
				publish_date=pub_date
			)
			
			ROIC_score = score_data[0].ROIC_score
			ROA_score = score_data[0].ROA_score
			EM_score = score_data[0].EM_score
			cash_flow_score = score_data[0].cash_flow_score
			dept_paying_score = score_data[0].dept_paying_score
			
			r.cash_adequancy_ratio = sum_act / (sum_pay + inventories_end - inventories_start)
			r.roic_score = ROIC_score
			r.roa_score = ROA_score
			r.em_score = EM_score
			r.cash_flow_score = cash_flow_score
			r.dept_paying_score = r.dept_paying_score
			r.save()

		
		