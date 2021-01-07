from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.forms.models import model_to_dict
from bs4 import BeautifulSoup
from django.db.models import Q
from django.db import transaction
from django.core.mail import send_mail
from django.core import serializers
from gjsicence import settings
from django.http import QueryDict
from .verification import VerificationCodeManager, TokenManager, create_default_avatar
from django.forms.models import model_to_dict
import json
import requests
import hashlib
import os
import redis
import datetime
import pymongo
import tushare as ts
from decimal import *
from .models import create_16_code, create_64_code, UserProfile, default_avatar, StockComments, FinancialStatement, FakeWallet, FakeStock, TransactionRecord
from .models import IncomeStatement, BalanceStatement, CashFlowStatement, FinancialAnalytical, OptionalShares, OptionalSharesItem, OptionalSharesGroup, OptionalSharesOprateCover, Stock
from .verification import pool, cursor
from concurrent.futures import ThreadPoolExecutor
PRO = ts.pro_api(token="df36b05825c5f945cdd1b566f85f69d6db45e597765a0bdc9f616f44")
STOCK_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
TRADE_CALENDAR_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
# Create your views here.
#token = "c3ebbfac31ace68059c0acae3c76eff6a391d09fa59fd20849fca141"
#ts.set_token(token)
#pro = ts.pro_api()
client = pymongo.MongoClient("mongodb://localhost:27017/")
indexdb = client["index"]
targetdb = client["resultdb"]
dailydb = client["daylinedb"]

verification_manager = VerificationCodeManager()
token_manager = TokenManager()


class GuanChaZheNewsParser(View):

    def get(self, request):
        news_html = requests.get("https://www.guancha.cn/economy?s=dhcaijing")
        news_html.encoding = 'utf8'
        soup = BeautifulSoup(news_html.text, "html.parser")
        news_list = []
        for news in soup.find_all("li", class_="fix"):
            news_ = {
                "href": news.a["href"],
                "img": news.a.img["src"],
                "title": news.div.h4.a.string,
                "summary": news.div.p.text[:-4],
                "date": news.div.div.span.string
            }
            news_list.append(news_)
        # print(json.dumps(news_list))
        return HttpResponse(json.dumps(news_list))


class TushareNewsParser(View):
    def get(self, request):
        news_html = requests.get("https://interface.sina.cn/finance/api_stock_sdyj.d.json?page=1&pagesize=10&callback=sinajp_159333602797212822217380178258")
        news_html.encoding = 'utf8'
        # print(json.loads(news_html.text.split("(")[1].split(")")[0])["result"]["data"])
        news_list = json.loads(news_html.text.split("(")[1].split(")")[0])["result"]["data"]
        news_data = []
        for news in news_list:
            data = {
                "title": news["title"],
                "url": news["url"],
                "source": news["source"],
                "time": news["time"],
            }
            news_data.append(data)
        # print(news_data)
        return HttpResponse(json.dumps(news_data))


class SearchAssociation(View):

    def get(self, request):
        # print(request.GET)
        raw_input = request.GET.get("input")
        filter = request.GET.get("filter", None)
        target_url = "https://smartbox.gtimg.cn/s3/?v=2&q=" + raw_input + "&t=all&c=1"
        # print(requests.get(target_url).text.encode('utf-8').decode("unicode_escape"))
        result = requests.get(target_url).text.encode('utf-8').decode("unicode_escape").split("v_hint=")[1].split('"')[1].split("^")
        # print(result)
        result_data = []
        exchange_dict = {
            "sh": "上海",
            "sz": "深圳",
            "hk": "香港",
            "us": "美国",
        }
        for stock in result:
            stock_info_list = stock.split("~")

            try:
                stock_data = {
                    "exchange": exchange_dict[stock_info_list[0]],
                    "exchange_abbr": stock_info_list[0],
                    "stock": stock_info_list[1],
                    "name": stock_info_list[2],
                    "isIndex": stock_info_list[-1]
                }

                if not filter:
                    result_data.append(stock_data)

                if filter == "hs" and (stock_data["exchange_abbr"] == "sz" or stock_data["exchange_abbr"] == "sh"):
                    result_data.append(stock_data)

                print(stock_data, filter)
                

            except KeyError:
                continue
        # print(result_data)
        return HttpResponse(json.dumps(result_data))


class StockStatus(View):

    def get(self, request):
        stock = request.GET.get("fullStock")[2:]
        market = request.GET.get("fullStock")[0:2]

        url_dict = {
            "sh": "http://web.ifzq.gtimg.cn/appstock/app/Minute/query?code=" + market + stock,
            "sz": "http://web.ifzq.gtimg.cn/appstock/app/Minute/query?code=" + market + stock,
            "hk": "http://web.ifzq.gtimg.cn/appstock/app/HkMinute/query?code=" + market + stock,
            "us": "http://web.ifzq.gtimg.cn/appstock/app/UsMinute/query?code=" + market + stock,
        }

        # print("http://web.ifzq.gtimg.cn/appstock/app/Minute/query?code=" + market + stock)
        html = requests.get(url_dict[market]).text
        # print(html)
        return HttpResponse(html)


class StockInfoFromSina(View):

    def get(self, request):
        stock = request.GET.get("stock")
        ret = StockInfoFromSina.get_stock_info(stock)
        return HttpResponse(ret)

    @staticmethod
    def get_stock_info(stock):
        target_url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/000651.phtml"
        # target_url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/000651.phtml"
        html = requests.get(target_url).text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())
        return soup.find_all(id="comInfo1")


class UserProfileUpdateManager(View):
    
    def patch(self, request):
        print(json.loads(request.body))
        new_name = json.loads(request.body)["name"]
        user_code = json.loads(request.body)["code"]
        print(user_code)
        UserProfile.objects.filter(
            user_code=user_code,
        ).update(nickname_str = new_name)
        return HttpResponse(new_name)


class UserProfileManager(object):

    @staticmethod
    def password_to_hash(password):
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def create(type_, code, password):
        type_dict = {
            "email": "UserProfile.objects.create(email_str=code,password_str=UserProfileManager.password_to_hash(password))",
            "phone": "UserProfile.objects.create(phone_str=code,password_str=UserProfileManager.password_to_hash(password))",
            "wx": "UserProfile.objects.create(wx_str=code,password_str=UserProfileManager.password_to_hash(password))"
        }
        return eval(type_dict[type_])

    @staticmethod
    def get(code, password):
        user_profile = UserProfile.objects.filter((Q(phone_str=code) | Q(wx_str=code) | Q(email_str=code)) & Q(password_str=UserProfileManager.password_to_hash(password)))
        return user_profile

    @staticmethod
    def is_exist(code):
        user_profile = UserProfile.objects.filter(Q(phone_str=code) | Q(email_str=code) | Q(wx_str=code))
        if user_profile:
            return True
        else:
            return False


class LoginStatusManager(View):

    def post(self, request):
        code = request.POST.get("code")
        password = request.POST.get("password")
        print(code)
        user_profile = UserProfileManager.get(code, password)
        if user_profile:
            token_manager.create(user_profile.values()[0]["user_code"])
            token = token_manager.get(user_profile.values()[0]["user_code"])
            return HttpResponse(json.dumps([200, user_profile.values()[0], token.decode("utf-8")]))
        else:
            return HttpResponse(json.dumps([404, None]))

    @token_manager.check
    def get(self, request):
        code = request.GET.get("code")
        user_profile = UserProfile.objects.filter(user_code=code)
        if user_profile:
            return HttpResponse(user_profile[0].nickname_str)
        else:
            return HttpResponse(json.dumps([500, None]))


class RegisterStatusManager(View):

    @staticmethod
    def pre_email_register(request):
        email = request.POST.get("email")
        user_profile = UserProfileManager.is_exist(email)
        if user_profile:
            return HttpResponse(json.dumps([500, None]))
        else:
            verification_manager.set_email("email", email)
            msg = "【高街科技】您的邮箱注册验证码为: " + verification_manager.get("email", email)[1].decode("utf-8") + "，有效时间10分钟。"
            send_mail(
                subject='【高街科技】邮箱注册',
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return HttpResponse(json.dumps([200, None]))

    @staticmethod
    def pre_email_change(request):
        email = request.POST.get("email")
        user_profile = UserProfileManager.is_exist(email)
        if not user_profile:
            return HttpResponse(json.dumps([500, None]))
        else:
            verification_manager.set_email("email", email)
            msg = "【高街科技】您正在修改账号密码，验证码为: " + verification_manager.get("email", email)[1].decode("utf-8") + "，有效时间10分钟。"
            send_mail(
                subject='【高街科技】修改密码',
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return HttpResponse(json.dumps([200, None]))

    @staticmethod
    def email_register(request, verification_code):
        email = request.POST.get("email")
        password = request.POST.get("password")
        verification_code_true = verification_manager.get("email", email)[1].decode("utf-8")
        if verification_code_true == verification_code:
            UserProfileManager.create("email", email, password)
            return HttpResponse(json.dumps([200, email]))
        else:
            return HttpResponse(json.dumps([500, None]))

    @staticmethod
    def email_change(patch, verification_code):
        email = patch.get("email")
        password = patch.get("password")
        verification_code_true = verification_manager.get("email", email)[1].decode("utf-8")
        if verification_code_true == verification_code:
            user_profile = UserProfile.objects.get(
                email_str=email
            )
            user_profile.password_str = UserProfileManager.password_to_hash(password)
            user_profile.save()
            return HttpResponse(json.dumps([200, email]))
        else:
            return HttpResponse(json.dumps([500, None]))

    def post(self, request):
        type_dict = {
            "email": "RegisterStatusManager.email_register(request, verification_code)",
            "pre_email": "RegisterStatusManager.pre_email_register(request)",
            "pre_change_email": "RegisterStatusManager.pre_email_change(request)"
        }
        type_ = request.POST.get("type")
        verification_code = request.POST.get("code")
        print(type_, verification_code)
        if verification_code:
            return eval(type_dict[type_])
        else:
            return eval(type_dict["pre_"+type_])

    def put(self, request):
        patch = QueryDict(request.body)
        type_dict = {
            "change_email": "RegisterStatusManager.email_change(patch, verification_code)",
        }
        type_ = patch.get("type")
        verification_code = patch.get("code")
        if verification_code:
            return eval(type_dict[type_])
        else:
            return eval(type_dict["pre_" + type_])


class CommentsManager(View):

    @staticmethod
    def get_today_comments(request, stock, range_):
        today_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        comments = json.loads(serializers.serialize("json", StockComments.objects.filter(stock_code=stock, create_date__gt=today_date)))
        for comment in comments:
            user_profile = UserProfile.objects.get(user_code=comment["fields"]["user_code"])
            comment["fields"]["avatar"] = user_profile.avatar_str
            comment["fields"]["nick"] = user_profile.nickname_str
        if len(comments) >= range_[1]:
            return comments[range_[0], range_[1]]
        else:
            return comments

    def get(self, request):
        type_ = request.GET.get("type")
        stock = request.GET.get("stock")
        page = int(request.GET.get("page"))
        range_ = ((page-1)*10, page*10-1)
        if type_ == "today":
            return HttpResponse(json.dumps(CommentsManager.get_today_comments(request, stock, range_)))

    def post(self, request):
        user_code = request.POST.get("user")
        stock_code = request.POST.get("stock")
        content_html = bytes(request.POST.get("content"), "utf-8")
        create_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        html_name = user_code + "-" + stock_code + "-" + create_date + ".html"
        html_path = os.path.join(settings.BASE_DIR, "media/commentHTML/" + html_name)
        with open(html_path, "wb") as html:
            html.write(content_html)
            ok = StockComments.objects.create(user_code=user_code, stock_code=stock_code, content_html="media/commentHTML/" + html_name)
        if ok:
            return HttpResponse(200)
        else:
            return HttpResponse(500)


class FinancialDataManager(View):

    def get(self, request):
        symbol = request.GET.get("symbol")
        date = request.GET.get("date")

        data = list(targetdb[symbol].find({"publish_date": date}))
        if len(data) >0:
            data[0].pop("_id")
            return HttpResponse(json.dumps(data[0]))
        else:
            return HttpResponse(404)

        #res = {
        #        "cash_flow_score": cash_flow_score,  # 现金流能力分数
        #        "cash_to_assets_ratio": cash_to_assets_ratio,  # 现金与约当现金比率
        #        "operation_cash_flow_ratio": operation_cash_flow_ratio,  # 现金流量比率
        #        "cash_adequancy_ratio": cash_adequancy_ratio,  # 现金允当比率
        #        "crir": crir,  # 现金再投资比率
        #        "accounts_receiv_turnover": accounts_receiv_turnover,  # 应收账款周转天数
        #        "income_score": income_score,  # 盈利能力分数
        #        "gross_profit_margin": gross_profit_margin,  # 毛利率
        #        "cost_rate": cost_rate,  # 费用率
        #        "income_rate": income_rate,  # 净利率
        #        "roe": roe,  # 总资产回报率
        #        "basic_eps": basic_eps,  # 每股收益
        #        "business_score": business_score,  # 运营能力分数
        #        "total_assets_turnover": total_assets_turnover,  # 总资产周转天数
        #        "inventories_turnover": inventories_turnover,  # 存货周转天数
        #        "business_days": business_days,  # 完整生意周期
        #        "kmpr": kmpr,  # 缺钱天数
        #        "em_score": em_score,  # 财务结构分数
        #        "debt_to_assets_ratio": debt_to_assets_ratio,  # 负债占资产比率
        #        "longterm_assets_to_fix_assets_ratio": longterm_assets_to_fix_assets_ratio,  # 长期资金占不动产及设备比率
        #        "dept_score": dept_score,  # 偿债能力分数
        #        "quick_ratio": quick_ratio,  # 速动比率
        #        "roic_score": roic_score,  # 速动比率
        #        "roa_score": roa_score,  # 速动比率
        #        "em_score_": em_score_,  # 速动比率
        #    }

        #    return HttpResponse(json.dumps(res))
        #else:

        #financial_statement = FinancialAnalytical.objects.filter(
        #    stock_code=symbol,
        #    publish_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
        #)

        #if financial_statement:
        #    data = financial_statement[0]
        #    cash_flow_score = 0  # 现金流能力
        #    roic_score = float(data.roic_score)
        #    roa_score = float(data.roa_score)
        #    em_score_ = float(data.em_score)
        #    # print(serializers.serialize("json", financial_statement))
        #    cash_to_assets_ratio = float(data.cash_to_assets_ratio)
        #    if cash_to_assets_ratio > 0.25:
        #        cash_flow_score += 50
        #    elif 0.25 >= cash_to_assets_ratio > 0.2:
        #        cash_flow_score += 40
        #    elif 0.20 >= cash_to_assets_ratio > 0.15:
        #        cash_flow_score += 30
        #    elif 0.15 >= cash_to_assets_ratio > 0.1:
        #        cash_flow_score += 20
        #    elif 0.1 >= cash_to_assets_ratio > 0:
        #        cash_flow_score += 10
        #    else:
        #        cash_flow_score += 0

        #    operation_cash_flow_ratio = float(data.operation_cash_flow_ratio)
        #    cash_adequancy_ratio = float(data.cash_adequancy_ratio)
        #    crir = float(data.crir)
        #    accounts_receiv_turnover = float(data.accounts_receiv_turnover)

        #    if operation_cash_flow_ratio > 1 and cash_adequancy_ratio > 1 and crir > 0.1:
        #        cash_flow_score += 20
        #    elif operation_cash_flow_ratio < 0 and cash_adequancy_ratio < 0 and crir < 0:
        #        cash_flow_score += 0
        #    else:
        #        cash_flow_score += 10

        #    if accounts_receiv_turnover < 15:
        #        cash_flow_score += 30
        #    elif 15 < accounts_receiv_turnover < 30:
        #        cash_flow_score += 25
        #    elif 30 < accounts_receiv_turnover < 60:
        #        cash_flow_score += 20
        #    elif 60 < accounts_receiv_turnover < 90:
        #        cash_flow_score += 15
        #    elif 90 < accounts_receiv_turnover < 150:
        #        cash_flow_score += 10
        #    elif 150 < accounts_receiv_turnover < 180:
        #        cash_flow_score += 5
        #    else:
        #        cash_flow_score += 0

        #    income_score = 0

        #    gross_profit_margin = float(data.gross_profit_margin)
        #    cost_rate = float(data.cost_rate)
        #    income_rate = float(data.income_rate)
        #    roe = float(data.roe)
        #    basic_eps = float(data.basic_eps)

        #    if roe > 0.5:
        #        income_score += 40
        #    elif 0.4 < roe <= 0.5:
        #        income_score += 35
        #    elif 0.3 < roe <= 0.4:
        #        income_score += 30
        #    elif 0.2 < roe <= 0.3:
        #        income_score += 25
        #    elif 0.1 < roe <= 0.2:
        #        income_score += 20
        #    elif 0 < roe <= 0.1:
        #        income_score += 15
        #    else:
        #        income_score += 0

        #    if gross_profit_margin >= 0.7:
        #        income_score += 20
        #    elif 0.6 <= gross_profit_margin < 0.7:
        #        income_score += 18
        #    elif 0.5 <= gross_profit_margin < 0.6:
        #        income_score += 16
        #    elif 0.4 <= gross_profit_margin < 0.5:
        #        income_score += 14
        #    elif 0.3 <= gross_profit_margin < 0.4:
        #        income_score += 12
        #    elif 0.2 <= gross_profit_margin < 0.3:
        #        income_score += 10
        #    elif 0.1 <= gross_profit_margin < 0.2:
        #        income_score += 8
        #    elif 0 <= gross_profit_margin < 0.1:
        #        income_score += 6
        #    else:
        #        income_score += 0

        #    if income_rate >= 0.5:
        #        income_score += 20
        #    elif 0.4 <= income_rate < 0.5:
        #        income_score += 18
        #    elif 0.3 <= income_rate < 0.4:
        #        income_score += 16
        #    elif 0.2 <= income_rate < 0.3:
        #        income_score += 14
        #    elif 0.1 <= income_rate < 0.2:
        #        income_score += 12
        #    elif 0 <= income_rate < 0.1:
        #        income_score += 10
        #    else:
        #        income_score += 0

        #    if cost_rate <= 0.05:
        #        income_score += 10
        #    elif 0.05 < cost_rate <= 0.08:
        #        income_score += 8
        #    elif 0.08 < cost_rate <= 0.11:
        #        income_score += 6
        #    elif 0.11 < cost_rate <= 0.14:
        #        income_score += 4
        #    else:
        #        income_score += 2

        #    if basic_eps > 0:
        #        income_score += 10
        #    else:
        #        income_score += 0

        #    business_score = 0
        #    total_assets_turnover = float(data.total_assets_turnover)
        #    inventories_turnover = float(data.inventories_turnover)
        #    business_days = float(data.business_days)
        #    kmpr = float(data.kmpr)

        #    if total_assets_turnover >= 1.5:
        #        business_score += 5
        #    elif 1.2 <= total_assets_turnover < 1.5:
        #        business_score += 10
        #    elif 0.9 <= total_assets_turnover < 1.2:
        #        business_score += 15
        #    elif 0.6 <= total_assets_turnover < 0.9:
        #        business_score += 20
        #    elif 0.3 <= total_assets_turnover < 0.6:
        #        business_score += 25
        #    else:
        #        business_score += 30

        #    if inventories_turnover >= 150:
        #        business_score += 5
        #    elif 120 <= inventories_turnover < 150:
        #        business_score += 10
        #    elif 90 <= inventories_turnover < 120:
        #        business_score += 15
        #    elif 60 <= inventories_turnover < 90:
        #        business_score += 20
        #    elif 30 <= inventories_turnover < 60:
        #        business_score += 25
        #    else:
        #        business_score += 30

        #    if kmpr >= 50:
        #        business_score += 5
        #    elif 40 <= kmpr < 50:
        #        business_score += 10
        #    elif 30 <= kmpr < 40:
        #        business_score += 15
        #    elif 20 <= kmpr < 30:
        #        business_score += 20
        #    elif 10 <= kmpr < 20:
        #        business_score += 25
        #    else:
        #        business_score += 30

        #    em_score = 0

        #    debt_to_assets_ratio = float(data.debt_to_assets_ratio)
        #    longterm_assets_to_fix_assets_ratio = float(data.longterm_assets_to_fix_assets_ratio)

        #    if debt_to_assets_ratio >= 1:
        #        em_score += 0
        #    elif 0.9 <= debt_to_assets_ratio < 1:
        #        em_score += 5
        #    elif 0.8 <= debt_to_assets_ratio < 0.9:
        #        em_score += 10
        #    elif 0.7 <= debt_to_assets_ratio < 0.8:
        #        em_score += 15
        #    elif 0.6 <= debt_to_assets_ratio < 0.7:
        #        em_score += 20
        #    elif 0.5 <= debt_to_assets_ratio < 0.6:
        #        em_score += 25
        #    elif 0.4 <= debt_to_assets_ratio < 0.5:
        #        em_score += 30
        #    elif 0.3 <= debt_to_assets_ratio < 0.4:
        #        em_score += 35
        #    elif 0.2 <= debt_to_assets_ratio < 0.3:
        #        em_score += 40
        #    elif 0.1 <= debt_to_assets_ratio < 0.2:
        #        em_score += 45
        #    else:
        #        em_score += 50

        #    if longterm_assets_to_fix_assets_ratio >= 4:
        #        em_score += 50
        #    elif 3.5 <= longterm_assets_to_fix_assets_ratio < 4:
        #        em_score += 45
        #    elif 3 <= longterm_assets_to_fix_assets_ratio < 3.5:
        #        em_score += 40
        #    elif 2.5 <= longterm_assets_to_fix_assets_ratio < 3:
        #        em_score += 35
        #    elif 2 <= longterm_assets_to_fix_assets_ratio < 2.5:
        #        em_score += 30
        #    elif 1.5 <= longterm_assets_to_fix_assets_ratio < 2:
        #        em_score += 25
        #    elif 1 <= longterm_assets_to_fix_assets_ratio < 1.5:
        #        em_score += 20
        #    elif 0.5 <= longterm_assets_to_fix_assets_ratio < 1:
        #        em_score += 15
        #    elif 0 <= longterm_assets_to_fix_assets_ratio < 0.5:
        #        em_score += 10
        #    else:
        #        em_score += 0

        #    dept_score = 0
        #    quick_ratio = float(data.quick_ratio)

        #    if quick_ratio >= 3:
        #        dept_score += 90
        #    elif 2.5 < quick_ratio < 3:
        #        dept_score += 80
        #    elif 2.0 < quick_ratio < 2.5:
        #        dept_score += 70
        #    elif 1.5 < quick_ratio < 2.0:
        #        dept_score += 60
        #    elif 1.0 < quick_ratio < 1.5:
        #        dept_score += 50
        #    elif 0.5 < quick_ratio < 1:
        #        dept_score += 40
        #    else:
        #        dept_score += 30

        #    print(dept_score)

            


class OptionalSharesManager(View):

    def get(self, request):
        user_code = request.GET.get("userCode")
        target = OptionalShares.objects.filter(
            user_code=user_code,
        )
        if target:
            return HttpResponse(serializers.serialize("json", target))
        else:
            return HttpResponse(404)

    def post(self, request):
        print(3)
        user_code = request.POST.get("userCode")
        stock_code = request.POST.get("stockCode")
        stock_exchange = request.POST.get("exchange")
        stock_name = request.POST.get("stockName")
        
        target = OptionalShares.objects.filter(
            user_code=user_code,
            stock_code=stock_code
        )
        if target:
            return HttpResponse(500)
        else:
            OptionalShares.objects.create(
                user_code=user_code,
                stock_code=stock_code,
                exchange=stock_exchange,
                name_cn=stock_name
            )
            return HttpResponse(200)

    def delete(self, request):
        user_code = request.GET.get("userCode")
        stock_code = request.GET.get("stockCode")
        target = OptionalShares.objects.filter(
            user_code=user_code,
            stock_code=stock_code
        )
        if target:
            target.delete()
            return HttpResponse(200)
        else:
            return HttpResponse(404)


class OptionalSharesGroupManager(View):

    def get(self, request):
        group_name = request.GET.get("groupName", None)
        user_code = request.GET.get("userCode")
        if group_name:
            group = OptionalSharesGroup.objects.filter(
                user_code=user_code,
                group_name=group_name
            )
            if group:
                return HttpResponse(serializers.serialize("json", group[0]))
        else:
            group = OptionalSharesGroup.objects.filter(
                user_code=user_code,
            )
            return HttpResponse(serializers.serialize("json", group))

    def post(self, request):
        group_name = request.POST.get("groupName")
        exchange = request.POST.get("exchange")
        user_code = request.POST.get("userCode")
        print(2)
        group = OptionalSharesGroup.objects.filter(
            user_code=user_code,
            group_name=group_name
        )
        if group:
            return HttpResponse(500)
        else:
            OptionalSharesGroup.objects.create(
                user_code=user_code,
                group_name=group_name,
                exchange=exchange
            )
            check_group = OptionalSharesGroup.objects.get(
                user_code=user_code,
                group_name=group_name
            )
            if check_group:
                return HttpResponse(check_group.group_code)
            else:
                return HttpResponse(500)


class OptionalSharesItemManager(View):

    def get(self, request):
        group_code = request.GET.get("groupCode", None)
        group_codes = request.GET.get("groupCodes", None)
        stock_code = request.GET.get("stockCode", None)

        if group_codes:
            res_dict = {}
            for code in group_codes.split(","):
                if code:
                    items = OptionalSharesItem.objects.filter(
                        group_code=code
                    )
                    res_dict[code] = {}
                    for item in items:
                        res_dict[code][item.stock_code] = model_to_dict(item)
                        res_dict[code][item.stock_code]["create_date"] = item.create_date.strftime("%Y%m%d")
            return HttpResponse(json.dumps(res_dict))


        if stock_code and group_code:
            item = OptionalSharesItem.objects.filter(
                group_code=group_code,
                stock_code=stock_code
            )
            return HttpResponse(serializers.serialize("json", item[0]))

        if group_code:
            items = OptionalSharesItem.objects.filter(
                group_code=group_code
            )
            return HttpResponse(serializers.serialize("json", items))

        return HttpResponse(404)

    def post(self, request):
        group_code = request.POST.get("groupCode", None)
        stock_code = request.POST.get("stockCode", None)
        name_cn = request.POST.get("nameCN", None)
        exchange = request.POST.get("exchange", None)
        sale_price = float(request.POST.get("salePrice", None))
        now_volume = float(request.POST.get("nowVolume", None))
        user_code = request.POST.get("userCode", None)
        print(group_code)
        group = OptionalSharesGroup.objects.filter(
            group_code=group_code
        )
        if group:
            OptionalSharesItem.objects.create(
                  group_code=group_code,
                  stock_code=stock_code,
                  name_cn=name_cn,
                  exchange=exchange,
                  sale_price=sale_price,
                  now_volume=now_volume,
                  user_code=user_code      
            )
            
            return HttpResponse(200)
        else:
            return HttpResponse(404)


class OptionalSharesOprateCoverManager(View):

    def get(self, request):
        group_code = request.GET.get("groupCode", None)
        item_code = request.GET.get("stockCode", None)
        if stock_code:
            cover = OptionalSharesOprateCover.objects.filter(
                item_code=item_code
            )
            return HttpResponse(serializers.serialize("json", cover[0]))
        if group_code:
            cover = OptionalSharesOprateCover.objects.filter(
                group_code=group_code
            )
            return HttpResponse(serializers.serialize("json", cover[0]))
        return HttpResponse(404)

    def post(self, request):
        stock_code = request.POST.get("stockCode", None)
        change_type = request.POST.get("changeType", None)
        before_volume = request.POST.get("beforeVolume", None)
        now_volume = request.POST.get("nowVolume", None)
        sale_price = request.POST.get("salePrice", None)
        name_cn = request.POST.get("nameCN", None)
        
        group = OptionalSharesGroup.objects.filter(
            user_code=user_code,
            group_name=group_name
        )
        if group:
            OptionalSharesOprateCoverManager.objects.create(
                stock_code=stock_code,
                change_type=change_type,
                before_volume=before_volume,
                now_volume=now_volume,
                sale_price=sale_price,
                name_cn=name_cn
            )
            return HttpResponse(200)
        else:
            return HttpResponse(404)


class StockIndustrySearchManager(View):

    def get(self, request):
        stock_code = request.GET.get("stockCode")
        stock = Stock.objects.filter(
            symbol=stock_code    
        )
        print(stock[0])
        if stock:
            industry = stock[0].industry
            return HttpResponse(industry)
        else:
            return HttpResponse(404)

class StockDailyDataManager(View):
    @staticmethod
    def get_month_data(stock_codes, create_dates):
        stock_list = stock_codes.split(",")
        create_list = create_dates.split(",")
        month_ago = (datetime.datetime.now()+datetime.timedelta(days=-30)).strftime("%Y%m%d")
        index = 0
        res_dict = {}
        for stock in stock_list:
            if len(stock) != 0:
                if create_list[index] >= month_ago:
                    #sale_price = OptionalSharesItem.objects.filter(
                    #    group_code = group_code,
                    #    stock_code = stock_code
                    #)
                    #res_dict[stock[2:]] = sale_price[0].sale_price
                    query = {
	                    "date": create_list[index]
                    }
                    doc = list(dailydb[stock[2:]].find(query))
                else:
                    query = {
	                    "date": month_ago
                    }
                    doc = list(dailydb[stock[2:]].find(query))
                res_dict[stock[2:]] = doc[0]["close"]
        return res_dict


    def get(self, request):
        stock_code = request.GET.get("stockCode", None)
        date = request.GET.get("date", None)
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        stock_codes = request.GET.get("stockCodes", None)
        create_dates = request.GET.get("createDates", None)


        if create_dates:
            res_dict = StockDailyDataManager.get_month_data(stock_codes, create_dates)
            return HttpResponse(json.dumps(res_dict))

        if start and end:
            query = {
	            "symbol": stock_code,
	            "date": {
		            "$gte": start,
                    "$lte": end
	            }
            }
            docs = dailydb.find(query)
            return HttpResponse(docs)

        if date:
            res_list = []
            for stock in stock_codes.split(","):
                if len(stock) != 0:
                    query = {
	                    "symbol": stock[2:],
	                    "date": {
		                    "$gte": date,
	                    }
                    }
                    docs = list(dailydb[stock[2:]].find(query))
                    #print(docs)
                    res_list.append(docs[0]["close"])
            #print(res_list)
            return HttpResponse(json.dumps(res_list))

        return HttpResponse(500)


class FakeWalletManager(View):
    
    def get(self, request):
        wallet_code = request.GET.get("walletCode", None)
        user_code = request.GET.get("userCode", None)
        type = request.GET.get("type", None)
        stock_list = request.GET.get("stockList", None)

        if wallet_code:
            result = FakeWalletManager.get_wallet_by_code(wallet_code)

        if user_code:
            result = FakeWalletManager.get_wallet_by_user(user_code)

        return JsonResponse({"data": result})

    def post(self, request):
        user_code = request.POST.get("userCode")
        wallet_name = request.POST.get("nameCN", None)
        FakeWallet.objects.create(
            user_code=user_code,
            wallet_name=wallet_name
        )
        return HttpResponse(200)

    @staticmethod
    def get_wallet_by_user(user_code):
        res = FakeWallet.objects.filter(
            user_code=user_code    
        )
        if not res:
            FakeWallet.objects.create(
                user_code=user_code,
            )
            res = FakeWallet.objects.filter(
                user_code=user_code    
            )
        return [model_to_dict(wallet) for wallet in res]

    @staticmethod
    def get_wallet_by_code(wallet_code):
        res = FakeWallet.objects.filter(
            wallet_code=wallet_code
        )
        if res:
            return model_to_dict(res[0])
        else:
            return {"status": "404", "info": "找不到该数据"}


class TransactionManager(View):

    def get(self, request):
        wallet_code = request.GET.get("walletCode")
        date = datetime.datetime.strptime(request.GET.get("date"), "%Y-%m-%d")
        res = {}
        query = TransactionRecord.objects.filter(
            wallet_code=wallet_code,
            create_date__year=date.year,
            create_date__month=date.month,
            create_date__day=date.day,
        )
        for record in query:
            if record.item_code not in res.keys():
                res[record.item_code] = [model_to_dict(record)]
            else:
                res[record.item_code].append(model_to_dict(record))
        print(res)
        return JsonResponse(res)

    @transaction.atomic
    def craete_transaction(wallet_code, item_code, item_num, item_cost, transaction_type, transaction_sum, transaction_commission, item_name, transaction_mark, item_exchange):
        TransactionRecord.objects.create(
            wallet_code=wallet_code,
            item_code=item_code,
            item_num =item_num ,
            item_cost=item_cost,
            transaction_type=transaction_type,
            transaction_sum=transaction_sum,
            transaction_commission=transaction_commission,
            transaction_mark=transaction_mark
        )
        print(item_num, item_cost, transaction_sum, transaction_commission)
        wallet = FakeWallet.objects.filter(
            wallet_code=wallet_code
        )
        wallet.update(
            balance=wallet[0].balance + Decimal(str(transaction_sum + transaction_commission))
        )
        if item_code != "000000":
            stock = FakeStock.objects.filter(
                wallet_code=wallet_code,
                stock_code=item_code
            )
            if stock:
                stock.update(
                    cost=(stock[0].now_volume * stock[0].cost - transaction_sum - transaction_commission) / (stock[0].now_volume + item_num),
                    now_volume=stock[0].now_volume + item_num
                )
            else:
                FakeStock.objects.create(
                    wallet_code=wallet_code,
                    stock_code=item_code,
                    name_cn=item_name,
                    now_volume=item_num,
                    exchange=item_exchange,
                    cost=abs((transaction_sum + transaction_commission) / item_num)
                )

        return 200


    def post(self, request):
        wallet_code = request.POST.get("walletCode", None)
        item_code = request.POST.get("itemCode", None)
        item_exchange = request.POST.get("exchange", None)
        transaction_type = int(request.POST.get("transactionType", None))
        item_num = int(request.POST.get("itemNum", None)) if transaction_type == 0 else -int(request.POST.get("itemNum", None))
        item_cost = float(request.POST.get("itemCost", None))
        item_name = request.POST.get("itemName", None)
        transaction_sum = -item_num * item_cost
        transaction_mark = request.POST.get("mark", None)
        transaction_commission = -abs(transaction_sum * 1 / 1000)
        res = TransactionManager.craete_transaction(wallet_code, item_code, item_num, item_cost, transaction_type, transaction_sum, transaction_commission, item_name, transaction_mark, item_exchange)
        #res = 200
        if res == 200:
            return HttpResponse(200)
        else:
            return HttpResponse(500)


class StockSearch(View):

    def get(self, request):
        keyword = request.GET.get("keyword", None)
        result = Stock.objects.filter(
            Q(symbol__startswith=keyword) | Q(name_cn__startswith=keyword) | Q(name_en__startswith=keyword)    
        )[0:8]
        return HttpResponse(serializers.serialize("json", result))


#  交易日历
class TradeCalendarManager(View):
    #  服务启动时下载交易日历并缓存入redis
    @staticmethod
    def update_calendar(cursor):
        #start_date = int(str(date)[0:4] + "0101")
        #end_date = int(str(date)[0:4] + "1231")
        year_list = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", ]
        
        for year in year_list:
            df = PRO.query('trade_cal', start_date=year+"0101", end_date=year+"1231", fields='cal_date,is_open,pretrade_date')
            for line in df.values.tolist():
                cursor.zadd("trade_date", {str(line[0]): int(line[0])})
                data = {
                    "date": str(line[0]),
                    "status": str(line[1]),
                    "pre": str(line[2])
                }
                cursor.hmset(str(line[0])+"_", data)
        return 200

    def get(self, request):
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
        cursor = redis.Redis(connection_pool=TRADE_CALENDAR_POOL)
        #calendar = []
        calendar = [cursor.hgetall(str(date)+"_") for date in  cursor.zrangebyscore("trade_date", start, end)]
        return JsonResponse({"result": calendar})
TradeCalendarManager.update_calendar(redis.Redis(connection_pool=TRADE_CALENDAR_POOL))
        


class StockManager(View):

    def get(self, request):
        keyword = request.GET.get("keyword", None)
        symbols = request.GET.get("symbols", None)
        cursor = redis.Redis(connection_pool=STOCK_POOL)
        result = []
        # 股票搜索
        if keyword:
            result = StockManager.keyword_for_search(keyword, cursor)
        # 股票查询
        if symbols:
            result = StockManager.symbols_for_select(symbols, cursor)
        # 如果需要股票查询当前价格
        return JsonResponse({"data": result})

        # 模糊查找，用于股票搜索，接受关键词，匹配并返回列表 
    @staticmethod
    def keyword_for_search(keyword, cursor):
        result = []
        keyword = "*" + keyword + "*" + "_param"
        keys = cursor.keys(keyword)[0:8]
        if keys:
            result = [cursor.hgetall(k.split("_")[0]+"_info") for k in keys]
        return result

    # 精确查找，接受股票代码，返回列表，多个代码用“,”隔开
    @staticmethod
    def symbols_for_select(symbols, cursor):
        symbol_list = symbols.split(",")
        result = [cursor.hgetall(symbol+"_info") if cursor.hgetall(symbol+"_info") else {} for symbol in symbol_list]
        return result


#  股票行情数据
class StockMarketDataManager(View):
    
    def get(self, request):
        symbols = request.GET.get("symbols", None)
        current_price = request.GET.get("currentPrice", None)
        history_price = request.GET.get("historyPrice", None)
        timestamp = request.GET.get("timestamp", None)
        cursor = redis.Redis(connection_pool=STOCK_POOL)
        stock_list = StockManager.symbols_for_select(symbols, cursor)
        result = []

        if current_price:
            result = StockMarketDataManager.get_current_price(stock_list, timestamp, cursor)

        return JsonResponse({"data": result})

    @staticmethod
    def get_current_price(stock_list, timestamp, cursor):
        timestamp = int(timestamp)
        symbol_list = [stock["symbol"] for stock in stock_list]
        # 从redis获取股票当前价格信息，如果不存在，则添加该股票代码至任务参数
        task_symbols = ""  # 任务参数，用于获取股票当前价格信息
        for stock in stock_list:
            symbol = stock["symbol"]
            price_info = cursor.hmget(symbol+"_current", "timestamp", "price", "close", "open", "turnover", "volume", "change_ratio", "change", "pe_ratio")
            if not price_info[0]:
                task_symbols += stock["exchange"] + symbol+","
            else:
                stock["price"] = price_info
        #  从gu.qq.com获取股票当前价格信息并存入redis，设置失效时间为10s
        expire = 10
        if len(task_symbols) != 0:
            price_info_list= requests.get("https://qt.gtimg.cn/q=" + task_symbols).text.split(";")[0:-1]
            for info in price_info_list:
                info = info.split("~")
                info_dict = {
                    "timestamp": timestamp,
                    "stock": info[2],  # 股票代码
                    "price": info[3],  # 价格
                    "close": info[4],  # 昨收
                    "open": info[5],  # 今开
                    "turnover": info[6],  # 交易量
                    "volume": info[7],  # 交易额
                    "change_ratio": info[32],  # 涨跌幅
                    "change": info[31],  # 涨跌额
                    "pe_ratio": info[39]  # 市盈率
                }
                cursor.hmset(info_dict["stock"]+"_current", info_dict)
                cursor.expire(info_dict["stock"]+"_current", expire)
                #  维持原股票列表顺序，添加价格信息
                index = symbol_list.index(info_dict["stock"])
                stock_list[index]["price"] = cursor.hmget(info_dict["stock"] + "_current", "timestamp", "price", "close", "open", "turnover", "volume", "change_ratio", "change", "pe_ratio")
        return stock_list

    @staticmethod
    def getAllStock(cursor):
        df = PRO.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,enname,fullname,market,list_status,delist_date')
        for stock in df.values.tolist():
            data = {
                "exchange": stock[0].split(".")[1].lower(),
                "symbol": stock[1],
                "name_cn": stock[2],
                "name_en": stock[6],
                "name_full": stock[5],
                "area": stock[3],
                "industry": stock[4],
                "market": stock[7],
                "list_status": stock[8],
                "list_date": stock[9],
                "delist_date": stock[10] if stock[10] else ""
            }
            cursor.set(data["symbol"]+ "_" + data["name_full"] + "_" + data["name_en"] + "_param", data["symbol"])
            cursor.hmset(data["symbol"] + "_info", data)

StockMarketDataManager.getAllStock(redis.Redis(connection_pool=TRADE_CALENDAR_POOL))