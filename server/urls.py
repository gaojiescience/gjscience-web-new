"""hs300 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import GuanChaZheNewsParser, TushareNewsParser, SearchAssociation, StockStatus, StockInfoFromSina, RegisterStatusManager, LoginStatusManager
from .views import CommentsManager
# from .views import Kline

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'news', GuanChaZheNewsParser.as_view(), name="news"),
    url(r'current', TushareNewsParser.as_view(), name="current"),
    url(r'searchAssociation', SearchAssociation.as_view(), name="searchAssociation"),
    url(r'stockStatus', StockStatus.as_view(), name="StockStatus"),
    url(r'stockInfo', StockInfoFromSina.as_view(), name="StockInfo"),
    url(r'register', RegisterStatusManager.as_view(), name="register"),
    url(r'login', LoginStatusManager.as_view(), name="login"),
    url(r'comments', CommentsManager.as_view(), name="comments"),
    # url(r'kline', Kline.as_view(), name='kline'),
]
