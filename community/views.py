from django.shortcuts import render, HttpResponse
from django.views.generic import View
import pymongo
import datetime
import json
from django.core import serializers

# Create your views here.
hs300 = pymongo.MongoClient('mongodb://localhost:27017/')['hs300']
hk50 = pymongo.MongoClient('mongodb://localhost:27017/')['hk50']


class Kline(View):

    def get(self, request):
        method = request.GET.get("method")
        methods_dict = {
            "daily": "Kline.get_daily_data(request)",
            "growth": "Kline.most_growth(request)"
        }
        # print(1)
        return HttpResponse(eval(methods_dict[method]))

    @staticmethod
    def get_daily_data(request):
        stock = request.GET.get("stock")
        start = request.GET.get("start")
        end = request.GET.get("end")
        col = hs300[stock]
        data = []
        days = []
        for line in col.find({"date": {"$gte": datetime.datetime(int(start.split("-")[0]), int(start.split("-")[1]),
                                                                 int(start.split("-")[2])).isoformat(),
                                       "$lt": datetime.datetime(int(end.split("-")[0]), int(end.split("-")[1]),
                                                                int(end.split("-")[2])).isoformat()}}):
            if line["tradeStatus"] == "1":
                data.append([float(line["open"]), float(line["close"]), float(line["low"]), float(line["high"])])
                days.append(line["date"].split("T")[0])
        return json.dumps({
            "days": days,
            "data": data
        })

    @staticmethod
    def most_growth(request):

        start = request.GET.get("start")
        end = request.GET.get("end")
        top = request.GET.get("top")
        sort = request.GET.get("sort")
        area = request.GET.get("area")
        col_dict = {}
        db = hs300 if area == "hs300" else hk50
        col_list = db.list_collection_names()
        for col in col_list:
            line_list = db[col].find({"date": {"$gte": datetime.datetime(int(start.split("-")[0]), int(start.split("-")[1]), int(start.split("-")[2])).isoformat(),
                                       "$lt": datetime.datetime(int(end.split("-")[0]), int(end.split("-")[1]), int(end.split("-")[2])).isoformat()}})
            start_line = line_list[0]
            end_line = line_list.sort([({
                "date", -1
            })])[0]
            increase = float(end_line["close"]) - float(start_line["close"])

            col_dict[col] = {
                "stock": start_line["stock"],
                "name": start_line["name"],
                # "start_price": float(start_line["close"]),
                # "end_price": float(end_line["close"]),
                # "increase": increase,
                "rate_of_increase": round((increase/float(start_line["close"]) * 100), 2)
            }

        price_list = [val for val in col_dict.values()]
        price_list.sort(key=lambda x: x["rate_of_increase"])
        # print(price_list)
        if sort == "0":
            # print(json.dumps(price_list[0: int(top)]))
            return json.dumps(price_list[0: int(top)])
        else:
            # print(json.dumps(price_list[-int(top)-1: -1]))
            return json.dumps(price_list[-int(top)-1: -1])
