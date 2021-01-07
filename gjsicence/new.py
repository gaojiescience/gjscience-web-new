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
		financial_statement = FinancialStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		income_statement = IncomeStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		balance_statement = BalanceStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		cash_statement = CashFlowStatement.objects.filter(
			stock_code=symbol,
			publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
		)

		if balance_statement and income_statement and cash_statement:
			try:
				balance_statement = balance_statement[0]
				income_statement = income_statement[0]
				cash_statement = cash_statement[0]
				balance_data = json.loads(json.loads(balance_statement.statement_content))
				income_data = json.loads(json.loads(income_statement.statement_content))
				cash_data = json.loads(json.loads(cash_statement.statement_content))
				money_cap = balance_data["money_cap"]["0"] if balance_data["money_cap"]["0"] else 0  # 货币资金
				trad_asset = balance_data["trad_asset"]["0"] if balance_data["trad_asset"]["0"] else 0  # 交易性金融资产
				total_cur_liab = balance_data["total_cur_liab"]["0"] if balance_data["total_cur_liab"]["0"] else 0  # 流动负债合计
				total_cur_assets = balance_data["total_cur_assets"]["0"] if balance_data["total_cur_assets"]["0"] else 0  # 流动资产合计
				total_liab = balance_data["total_liab"]["0"] if balance_data["total_liab"]["0"] else 0  # 负债合计
				accounts_receiv = balance_data["accounts_receiv"]["0"] if balance_data["accounts_receiv"]["0"] else 0  # 应收账款
				acct_payable = balance_data["acct_payable"]["0"] if balance_data["acct_payable"]["0"] else 0  # 应付账款
				inventories = balance_data["inventories"]["0"] if balance_data["inventories"]["0"] else 0  # 期末存货
				total_hldr_eqy_inc_min_int = balance_data["total_hldr_eqy_inc_min_int"]["0"] if balance_data["total_hldr_eqy_inc_min_int"]["0"] else 0  # 股东权益合计
				total_ncl = balance_data["total_ncl"]["0"] if balance_data["total_ncl"]["0"] else 0  # 非流动负债合计
				fix_assets = balance_data["fix_assets"]["0"] if balance_data["fix_assets"]["0"] else 0  # 固定资产
				cip = balance_data["cip"]["0"] if balance_data["cip"]["0"] else 0  # 在建工程
				const_materials = balance_data["const_materials"]["0"] if balance_data["const_materials"]["0"] else 0  # 工程物资
				longterm_assets_to_fix_assets_ratio = (total_ncl + total_hldr_eqy_inc_min_int) / (const_materials + fix_assets + cip)  # 长期资金占不动产及设备比率

				n_cashflow_act = cash_data["n_cashflow_act"]["0"] if cash_data["n_cashflow_act"]["0"] else 0  # 营业活动产生的现金流量净额
				c_fr_sale_sg = cash_data["c_fr_sale_sg"]["0"] if cash_data["c_fr_sale_sg"]["0"] else 0  # 销售收入
				decr_inventories = cash_data["decr_inventories"]["0"] if cash_data["decr_inventories"]["0"] else 0  # 存货的减少
				c_pay_dist_dpcp_int_exp = cash_data["c_pay_dist_dpcp_int_exp"]["0"] if cash_data["c_pay_dist_dpcp_int_exp"]["0"] else 0  # 现金股利
				total_assets = balance_data["total_assets"]["0"] if balance_data["total_assets"]["0"] else 0  # 总资产
				crir = (n_cashflow_act - c_pay_dist_dpcp_int_exp) / (total_assets - total_cur_liab)  # 现金再投资比率

				revenue = income_data["revenue"]["0"] if income_data["revenue"]["0"] else 0  # 营业收入
				total_revenue = income_data["total_revenue"]["0"] if income_data["total_revenue"]["0"] else 0  # 营业总收入
				oper_cost = income_data["oper_cost"]["0"] if income_data["oper_cost"]["0"] else 0  # 营业成本
				total_cogs = income_data["total_cogs"]["0"] if income_data["total_cogs"]["0"] else 0  # 营业总成本
				sell_exp = income_data["sell_exp"]["0"] if income_data["sell_exp"]["0"] else 0  # 销售费用
				admin_exp = income_data["admin_exp"]["0"] if income_data["admin_exp"]["0"] else 0  # 管理费用
				fin_exp = income_data["fin_exp"]["0"] if income_data["fin_exp"]["0"] else 0  # 财务费用
				n_income = income_data["n_income"]["0"] if income_data["n_income"]["0"] else 0  # 净利润
				gross_profit_margin = (revenue - oper_cost) / revenue  # 毛利率
				cost_rate = (sell_exp + admin_exp + fin_exp) / total_cogs  # 费用率
				income_rate = n_income / revenue  # 利润率
				basic_eps = income_data["basic_eps"]["0"] if income_data["basic_eps"]["0"] else 0  # 每股收益
				roe = n_income / (total_assets - total_liab)  # 净资本收益率
				total_assets_turnover = total_revenue / total_assets  # 总资本周转率
				accounts_receiv_turnover = accounts_receiv * 365 / revenue  # 应收账款周转天数
				acct_payable_turnover = acct_payable * 365 / revenue  # 应付账款周转天数
				inventories_turnover = 360 / (oper_cost / inventories)  # 存货周转天数
				inventories_days = accounts_receiv_turnover + inventories_turnover  # 库存天数
				business_days = inventories_days + accounts_receiv_turnover  # 完整生意周期
				kmpr = business_days - acct_payable_turnover  # 缺钱天数
				debt_to_assets_ratio = total_liab / total_assets  # 负债占资产比率
				quick_ratio = (total_cur_assets - inventories) / total_cur_liab  # 速动比率
				cash_to_assets_ratio = (money_cap + trad_asset) / total_assets  # 现金与约当现金比率
				
				if not FinancialAnalytical.objects.filter(
					stock_code=symbol,
					publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
				).exists():
					FinancialAnalytical.objects.create(
						stock_code=symbol,
						exchange=stock.exchange,
						publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])),
						cash_to_assets_ratio=cash_to_assets_ratio,
						crir=crir,
						# cash_adequancy_ratio=cash_adequancy_ratio,
						accounts_receiv_turnover=accounts_receiv_turnover,
						gross_profit_margin=gross_profit_margin,
						cost_rate=cost_rate,
						income_rate=income_rate,
						roe=roe,
						basic_eps=basic_eps,
						total_assets_turnover=total_assets_turnover,
						inventories_turnover=inventories_turnover,
						business_days=business_days,
						kmpr=kmpr,
						debt_to_assets_ratio=debt_to_assets_ratio,
						longterm_assets_to_fix_assets_ratio=longterm_assets_to_fix_assets_ratio,
						quick_ratio=quick_ratio
					)
			except ZeroDivisionError:
				pass
			except KeyError:
				pass
				
				