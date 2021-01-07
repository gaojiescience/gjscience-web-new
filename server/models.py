import os
# import JSONField
from django.contrib.postgres.fields import JSONField
from django.db import models
from .verification import create_16_code, create_64_code
from gjsicence import settings


# Create your models here.
default_avatar = os.path.join(settings.BASE_DIR, "media/avatar/default_avatar.jpg")
html_root = os.path.join(settings.BASE_DIR, "media/comments/")
print(default_avatar)


class UserProfile(models.Model):

    user_code = models.CharField("用户编号", max_length=255, null=False, blank=False, unique=True, default=create_16_code)
    phone_str = models.CharField("手机号码", max_length=255, null=True, blank=True, unique=True)
    nickname_str = models.CharField("用户名", max_length=16, null=False, blank=False, default="匿名用户")
    password_str = models.CharField("密码", max_length=255, null=False, blank=False)
    wx_str = models.CharField("微信账号", max_length=255, null=True, blank=True, unique=True)
    avatar_str = models.CharField("头像地址", max_length=255, null=True, blank=True, default=default_avatar)
    email_str = models.CharField("用户邮箱", max_length=255, null=True, blank=True, unique=True)
    email_tips_active = models.IntegerField("是否激活邮箱提醒", null=False, blank=False, default=0)

    class Meta:
        db_table = "UserProfile"


class StockComments(models.Model):

    comment_code = models.CharField("评论编号", max_length=255, null=False, blank=False, unique=True, default=create_16_code)
    user_code = models.CharField("绑定用户编号", max_length=255, null=False, blank=False)
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    content_html = models.CharField("评论内容html路径", max_length=255)
    create_date = models.DateTimeField("创建时间", auto_now_add=True)
    change_date = models.DateTimeField("最后修改时间", auto_now=True)


class FinancialStatement(models.Model):

    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    publish_date = models.DateTimeField("公布时间")
    statement_content = models.TextField()
    ROIC_score = models.CharField("投资回报率得分", max_length=255, null=True, blank=True)
    ROA_score = models.CharField("总资产报酬率得分", max_length=255, null=True, blank=True)
    EM_score = models.CharField("权益乘数得分", max_length=255, null=True, blank=True)
    cash_flow_score = models.CharField("现金流能力得分", max_length=255, null=True, blank=True)
    dept_paying_score = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)

    arturn_days = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    roa = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    roic = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    assets_to_eqt = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    ocf_to_debt = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    fixed_assets = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)
    cash_to_liqdebt = models.CharField("偿债能力得分", max_length=255, null=True, blank=True)


class Stock(models.Model):

    exchange = models.CharField("所属交易所", max_length=8)
    symbol = models.CharField("股票代码", max_length=16)
    name_cn = models.CharField("股票中文名", max_length=255, null=True, blank=True)
    name_en = models.CharField("股票英文名", max_length=255, null=True, blank=True)
    name_full = models.CharField("股票全称", max_length=255, null=True, blank=True)
    area = models.CharField("所在地区", max_length=255, null=True, blank=True)
    industry = models.CharField("所属行业", max_length=255, null=True, blank=True)
    market = models.CharField("所属市场", max_length=255, null=True, blank=True)
    list_status = models.CharField("交易状态", max_length=255, null=True, blank=True)
    list_date = models.CharField("上市时间", max_length=255, null=True, blank=True)
    delist_date = models.CharField("退市时间", max_length=255, null=True, blank=True)


class IncomeStatement(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    publish_date = models.DateTimeField("公布时间")
    statement_content = models.TextField()


class CashFlowStatement(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    publish_date = models.DateTimeField("公布时间")
    statement_content = models.TextField()


class BalanceStatement(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    publish_date = models.DateTimeField("公布时间")
    statement_content = models.TextField()


class FinancialAnalytical(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    publish_date = models.DateTimeField("公布时间")
    operation_cash_flow_ratio = models.CharField("现金流量比率", max_length=255, null=False, blank=False, default="123456")
    cash_to_assets_ratio = models.CharField("现金与现金约当比率", max_length=255, null=False, blank=False, default="123456")
    crir = models.CharField("现金再投资比率", max_length=255, null=False, blank=False, default="123456")
    cash_adequancy_ratio = models.CharField("现金允当比率", max_length=255, null=False, blank=False, default="123456")
    accounts_receiv_turnover = models.CharField("应收账款周转天数", max_length=255, null=False, blank=False, default="123456")
    gross_profit_margin = models.CharField("毛利率", max_length=255, null=False, blank=False, default="123456")
    cost_rate = models.CharField("费用率", max_length=255, null=False, blank=False, default="123456")
    income_rate = models.CharField("净利率", max_length=255, null=False, blank=False, default="123456")
    roe = models.CharField("净资本收益率", max_length=255, null=False, blank=False, default="123456")
    basic_eps = models.CharField("每股收益", max_length=255, null=False, blank=False, default="123456")
    total_assets_turnover = models.CharField("总资本周转率", max_length=255, null=False, blank=False, default="123456")
    inventories_turnover = models.CharField("存货周转天数", max_length=255, null=False, blank=False, default="123456")
    business_days = models.CharField("完整生意周期", max_length=255, null=False, blank=False, default="123456")
    kmpr = models.CharField("缺钱天数", max_length=255, null=False, blank=False, default="123456")
    debt_to_assets_ratio = models.CharField("负债占资产比率", max_length=255, null=False, blank=False, default="123456")
    longterm_assets_to_fix_assets_ratio = models.CharField("长期资金占不动产及设备比率", max_length=255, null=False, blank=False, default="123456")
    quick_ratio = models.CharField("速动比率", max_length=255, null=False, blank=False, default="123456")
    roic_score = models.CharField("roic分数", max_length=255, null=False, blank=False, default="123456")
    roa_score = models.CharField("roa分数", max_length=255, null=False, blank=False, default="123456")
    em_score = models.CharField("em分数", max_length=255, null=False, blank=False, default="123456")
    cash_flow_score = models.CharField("cash_flow分数", max_length=255, null=False, blank=False, default="123456")
    dept_paying_score = models.CharField("dept_paying分数", max_length=255, null=False, blank=False, default="123456")


class OptionalShares(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    name_cn = models.CharField("股票中文名", max_length=255, null=True, blank=True)
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    user_code = models.CharField("用户编号", max_length=255, null=False, blank=False, default=create_16_code)
    create_date = models.DateTimeField(auto_now=True)

class OptionalSharesItem(models.Model):
    item_code = models.CharField("自选股编号", max_length=255, null=False, blank=False, default=create_16_code)
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    name_cn = models.CharField("股票中文名", max_length=255, null=True, blank=True)
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    user_code = models.CharField("所属用户编号", max_length=255, null=False, blank=False, default=create_16_code)
    group_code = models.CharField("所属分组编号", max_length=255, null=False, blank=False, default=create_16_code)
    sale_price = models.FloatField("交易价格", null=False, blank=False, default=0)
    now_volume = models.FloatField("持有数量", null=False, blank=False, default=0)
    create_date = models.DateTimeField(auto_now=True)

class OptionalSharesGroup(models.Model):
    user_code = models.CharField("用户编号", max_length=255, null=False, blank=False, default=create_16_code)
    group_code = models.CharField("分组编号", max_length=255, null=False, blank=False, default=create_16_code)
    group_name = models.CharField("分组名称", max_length=255, null=False, blank=False, default="123456")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    create_date = models.DateTimeField(auto_now=True)


class OptionalSharesOprateCover(models.Model):
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    name_cn = models.CharField("股票中文名", max_length=255, null=True, blank=True)
    changeType = models.IntegerField("更改类型", null=False, blank=False, default=0) # 0 添加，1 增减，2 删除
    group_code = models.CharField("所属分组编号", max_length=255, null=False, blank=False, default=create_16_code)
    item_code = models.CharField("所属自选股编号", max_length=255, null=False, blank=False, default=create_16_code)
    before_volume = models.IntegerField("先前持有数量", null=False, blank=False, default=0)
    now_volume = models.IntegerField("当前持有数量", null=False, blank=False, default=0)
    sale_price = models.IntegerField("交易价格", null=False, blank=False, default=0)
    create_date = models.DateTimeField(auto_now=True)


class FakeWallet(models.Model):
    user_code = models.CharField("用户编号", max_length=255, null=False, blank=False, default=create_16_code)
    wallet_code = models.CharField("钱包编号", max_length=255, null=False, blank=False, default=create_16_code)
    wallet_name = models.CharField("钱包名称", max_length=255, null=False, blank=False, default="虚拟账号")
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")
    balance = models.DecimalField("账户余额", max_digits=12, decimal_places=2, null=False, blank=False, default=100000.00)
    create_date = models.DateTimeField(auto_now=True)


class TransactionRecord(models.Model):
    record_code = models.CharField("记录编号", max_length=255, null=False, blank=False, default=create_16_code)
    wallet_code = models.CharField("钱包编号", max_length=255, null=False, blank=False, default=create_16_code)
    item_code = models.CharField("交易对象代码", max_length=255, null=False, blank=False, default="000000")  # 000000为金钱
    item_num = models.IntegerField("交易对象数量")
    item_cost =  models.DecimalField("交易对象价格", max_digits=12, decimal_places=2)
    transaction_type = models.IntegerField("交易类型", null=False, blank=False, default=0)  # 0买入 1 卖出
    transaction_sum = models.DecimalField("交易金额", max_digits=12, decimal_places=2, null=False, blank=False, default=100000.00)
    transaction_commission = models.DecimalField("交易佣金", max_digits=12, decimal_places=2)
    transaction_mark = models.CharField("交易备注", max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)


class FakeStock(models.Model):
    wallet_code = models.CharField("钱包编号", max_length=255, null=False, blank=False, default=create_16_code)
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    name_cn = models.CharField("股票中文名", max_length=255, null=True, blank=True)
    now_volume = models.FloatField("持有数量", null=False, blank=False, default=0)
    cost = models.FloatField("持仓成本", null=False, blank=False, default=0)
    exchange = models.CharField("所属交易所", max_length=8, default="SZ")



