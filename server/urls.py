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
from .views import GuanChaZheNewsParser, TushareNewsParser, SearchAssociation, StockStatus, StockInfoFromSina, RegisterStatusManager, LoginStatusManager, FinancialDataManager, UserProfileUpdateManager
from .views import CommentsManager, OptionalSharesManager, OptionalSharesGroupManager, OptionalSharesItemManager, OptionalSharesOprateCoverManager, StockIndustrySearchManager, StockDailyDataManager
from .views import FakeWalletManager, TransactionManager, StockSearch, StockManager, TradeCalendarManager, StockMarketDataManager
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
    url(r'financial', FinancialDataManager.as_view(), name="financial"),
    url(r'optionalSharesGroup', OptionalSharesGroupManager.as_view(), name="OptionalSharesGroup"),
    url(r'optionalSharesItem', OptionalSharesItemManager.as_view(), name="optionalSharesItem"),
    url(r'optionalShares', OptionalSharesManager.as_view(), name="optionalShares"),  
    url(r'optionalSharesOprateCover', OptionalSharesOprateCoverManager.as_view(), name="optionalSharesOprateCover"),
    url(r'stockIndustry', StockIndustrySearchManager.as_view(), name="stockIndustry"),
    url(r'daily', StockDailyDataManager.as_view(), name="daily"),
    url(r'userProfile', UserProfileUpdateManager.as_view(), name="userprofile"),
    url(r'wallet', FakeWalletManager.as_view(), name="wallet"),
    url(r'transaction', TransactionManager.as_view(), name="transaction"),
    url(r'stockSearch', StockSearch.as_view(), name="stockSearch"),
    url(r'stockManager', StockManager.as_view(), name="stockManager"),
    url(r'tradeCalendar', TradeCalendarManager.as_view(), name="tradeCalendarManager"),
    url(r'stockMarketData', StockMarketDataManager.as_view(), name="stockMarketDataManager"),
    # url(r'kline', Kline.as_view(), name='kline'),
]
