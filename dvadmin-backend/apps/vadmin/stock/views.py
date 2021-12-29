import logging
from datetime import datetime, date
from decimal import Decimal

from rest_framework.request import Request
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.stock.models.index import Index
from apps.vadmin.stock.models.index_history import IndexHistory
from apps.vadmin.stock.serializers import IndexHistorySerializer, IndexSerializer
from chinese_calendar import is_workday, is_holiday
import akshare as ak
import numpy as np

import logging

# 生成一个以当前文件名为名字的logger实例
from apps.vadmin.utils import datetime_util

logger = logging.getLogger(__name__)


class IndexHistoryModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = IndexHistory.objects.all()
    serializer_class = IndexHistorySerializer

    # 获取某时间段的涨幅
    def get_time_period(self, request: Request, *args, **kwargs):
        results = []
        dates = request.data["dates"]
        # 循环指数
        for code in request.data["ids"]:
            # 指数是否为空 升序
            queryset = list(IndexHistory.objects.filter(code=code, date__range=dates).order_by("date"))
            # 判断是否有值
            if not queryset:
                self.__history_bUlk_add__(code, None)
                queryset = list(IndexHistory.objects.filter(code=code, date__range=dates).order_by("date"))
                self.__compute__(queryset, results)
            else:
                # 什么情况下补更 节假日   时间是否对应，排除今天
                # 判断最大的时间是否等于输入时间
                if queryset[len(queryset) - 1].date == datetime_util.string_2date(dates[1]) or is_holiday(
                        datetime_util.string_2date(dates[1])) or datetime_util.string_2date(dates[1]) != date.today():
                    # 计算出最大涨跌幅  (当天收盘价格-第一天收盘价格)/当天收盘价格
                    self.__compute__(queryset, results)
                else:
                    queryset += self.__history_bUlk_add__(code, queryset[len(queryset) - 1].date)
                    self.__compute__(queryset, results)
        return SuccessResponse(results)

    def __compute__(self, queryset, results):
        low = 0
        high = 0
        high_date = 0
        high_close = 0
        for x, index in enumerate(queryset):
            if x == 0:
                fist_close = index.close
            else:
                contrast = (fist_close - index.close) / fist_close
                if contrast < low:
                    low = contrast
                if contrast > high:
                    high = contrast
                    high_date = index.date
                    high_close = index.close

        return results.append({'name': queryset[0].name, 'high': (high * 100).quantize(Decimal('0.00')),
                               'highDate': high_date,
                               'highClose': high_close,
                               'fist_close': fist_close,
                               'low': (low * 100).quantize(Decimal('0.00'))})

    def __history_bUlk_add__(self, code, date):
        index = Index.objects.filter(code=code)[0]
        stock_zh_index_daily = ak.stock_zh_index_daily(index.code)
        daily_arr = []
        for x in stock_zh_index_daily.values:
            if not date:
                index_history = IndexHistory()
                index_history.code = index.code
                index_history.name = index.name
                index_history.date = x[0]
                index_history.open = x[1]
                index_history.high = x[2]
                index_history.low = x[3]
                index_history.close = x[4]
                index_history.volume = x[5]
                daily_arr.append(index_history)
            else:
                if datetime_util.string_2datetime2(date) < datetime_util.string_2datetime2(x[0]):
                    index_history = IndexHistory()
                    index_history.code = index.code
                    index_history.name = index.name
                    index_history.date = x[0]
                    index_history.open = x[1]
                    index_history.high = x[2]
                    index_history.low = x[3]
                    index_history.close = x[4]
                    index_history.volume = x[5]
                    daily_arr.append(index_history)
        return IndexHistory.objects.bulk_create(daily_arr)


class IndexModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

    # 查询指数名称
    def get_index_list(self, request: Request, *args, **kwargs):
        namelist = Index.objects.values_list("name", "code")
        return SuccessResponse(data={"code": [item[1] for item in namelist],
                                     "name": [item[0] for item in namelist]})

    # 初始数据
    def get_index_data(self, request: Request, *args, **kwargs):
        if Index.objects.exists():
            queryset = Index.objects.all()
            if queryset.first().create_datetime > datetime.today():
                queryset = self.__bUlk_add__()
            serializer = self.get_serializer(queryset, many=True)
            return SuccessResponse(serializer.data)
        else:
            queryset = self.__bUlk_add__()
            serializer = self.get_serializer(queryset, many=True)
            return SuccessResponse(serializer.data)

    def __bUlk_add__(self):
        Index.objects.all().delete()
        stock_zh_index_spot_df = ak.stock_zh_index_spot()
        index_arr = []
        for x in stock_zh_index_spot_df.values:
            index = Index()
            index.code = x[0]
            index.name = x[1]
            index.latest_price = x[2]
            index.change_percent = x[3]
            index.price_change = x[4]
            index.closed = x[5]
            index.open = x[6]
            index.height = x[7]
            index.low = x[8]
            index.volume = x[9]
            index.amount = x[10]
            index_arr.append(index)
        return Index.objects.bulk_create(index_arr)
