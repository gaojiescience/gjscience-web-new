from django.shortcuts import render, HttpResponse
from django.views.generic import View
from bs4 import BeautifulSoup
from django.db.models import Q
from django.core.mail import send_mail
from django.core import serializers
from gjsicence import settings
from .verification import VerificationCodeManager, TokenManager, create_default_avatar
import json
import requests
import hashlib
import os
import redis
import urllib.parse
import datetime
import tushare as ts
from .models import create_16_code, create_64_code, UserProfile, default_avatar, StockComments
from .verification import pool, cursor
# Create your views here.
token = "c3ebbfac31ace68059c0acae3c76eff6a391d09fa59fd20849fca141"
ts.set_token(token)
pro = ts.pro_api()

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
                result_data.append(stock_data)

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
        print(1)
        ret = StockInfoFromSina.get_stock_info(stock)
        return HttpResponse(ret)

    @staticmethod
    def get_stock_info(stock):
        target_url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/000651.phtml"
        # target_url = "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/000651.phtml"
        html = requests.get(target_url).text
        soup = BeautifulSoup(html, 'html.parser')

        print(soup.find_all(id="comInfo1"))
        # print(soup.prettify())
        return soup.find_all(id="comInfo1")


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
            return HttpResponse([500, None])
        else:
            verification_manager.set_email("email", email)
            msg = "【高街科技】您的邮箱注册验证码为: " + verification_manager.get("email", email)[1].decode("utf-8") + "，有效时间10分钟。"
            print(msg)
            send_mail(
                subject='【高街科技】邮箱注册',
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return HttpResponse([200, None])

    @staticmethod
    def email_register(request, verification_code):
        email = request.POST.get("email")
        password = request.POST.get("password")
        verification_code_true = verification_manager.get("email", email)[1].decode("utf-8")
        if verification_code_true == verification_code:
            UserProfileManager.create("email", email, password)
            return HttpResponse([200, email])
        else:
            return HttpResponse([500, None])

    def post(self, request):
        type_dict = {
            "email": "RegisterStatusManager.email_register(request, verification_code)",
            "pre_email": "RegisterStatusManager.pre_email_register(request)",
        }
        type_ = request.POST.get("type")
        verification_code = request.POST.get("code")
        if verification_code:
            return eval(type_dict[type_])
        else:
            return eval(type_dict["pre_"+type_])


class CommentsManager(View):

    @staticmethod
    def get_today_comments(request, stock, range_):
        today_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        comments = json.loads(serializers.serialize("json", StockComments.objects.filter(stock_code=stock, create_date__gt=today_date)))
        for comment in comments:
            user_profile = UserProfile.objects.get(user_code=comment["fields"]["user_code"])
            comment["fields"]["avatar"] = user_profile.avatar_str
            comment["fields"]["nick"] = user_profile.nickname_str
        print(comments)
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
