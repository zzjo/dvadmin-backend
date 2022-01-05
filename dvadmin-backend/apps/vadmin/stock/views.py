import decimal
import logging
from datetime import datetime, date
from decimal import Decimal

from rest_framework.request import Request
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.stock.models.index import Index
from apps.vadmin.stock.models.index_history import IndexHistory
from apps.vadmin.stock.models.new_fund import NewFund
from apps.vadmin.stock.serializers import IndexHistorySerializer, IndexSerializer, NewFundSerializer
from chinese_calendar import is_workday, is_holiday
import akshare as ak

import logging

# 生成一个以当前文件名为名字的logger实例
from apps.vadmin.utils import datetime_util

logger = logging.getLogger(__name__)


class NewFundModelViewSet(CustomModelViewSet):
    """
       菜单模型 的CRUD视图
       """
    queryset = NewFund.objects.all()
    serializer_class = NewFundSerializer

    # 获取新基金数据(按月份查找)
    def get_new_fund(self, request: Request, *args, **kwargs):
        # 判断是否更新
        newfund = NewFund.objects.all().order_by('-date_establishment')
        if newfund.exists():
            # 判断是今天是否更新过
            newfundlist = list(newfund)
            if newfundlist[0].create_datetime == datetime.today():
                pass
            else:
                # 更新缺失部分
                self.__add_new_fund__(newfundlist[0].date_establishment)
        else:
            self.__add_new_fund__(None)

    def __add_new_fund__(self, date_establishment):
        fund_em_new_found_df = ak.fund_em_new_found()
        dirdata = fund_em_new_found_df.to_dict('records')
        daily_arr = []
        if not date_establishment:
            for x in dirdata:
                self.__do_mapping__(daily_arr, x)
        else:
            for x in dirdata:
                if datetime_util.string_2date(x['成立日期']) > date_establishment:
                    self.__do_mapping__(daily_arr, x)
        return NewFund.objects.bulk_create(daily_arr)

    def __do_mapping__(self, arr, x):
        newfund = NewFund()
        newfund.name = x['基金简称']
        newfund.code = x['基金代码']
        newfund.date_establishment = x['成立日期']
        newfund.discount_rate = x['优惠费率']
        established_increase = x['成立来涨幅'].replace(',', '')
        newfund.established_increase = decimal.Decimal(0 if not established_increase else established_increase)
        newfund.fund_manager = x['基金经理']
        newfund.fund_type = x['基金类型']
        newfund.publisher = x['发行公司']
        raise_shares = x['募集份额'].replace(',', '')
        newfund.raise_shares = decimal.Decimal(0 if not raise_shares else raise_shares)
        newfund.subscription_period = x['集中认购期']
        newfund.subscription_status = x['申购状态']
        logger.info("募集份额{0}, 成立来涨幅{1}".format(newfund.raise_shares, newfund.established_increase))
        arr.append(newfund)


class IndexHistoryModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = IndexHistory.objects.all()
    serializer_class = IndexHistorySerializer

    # 获取历史数据
    def get_index_history(self, request: Request, *args, **kwargs):
        dates = request.data["dates"]
        code = request.data["code"]
        return SuccessResponse(
            IndexHistory.objects.filter(code=code, date__range=dates).values_list("date", "open", "close", "low",
                                                                                  'high'))

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
                if is_holiday(datetime_util.string_2date(dates[1])) or queryset[
                    len(queryset) - 1].date == datetime_util.string_2date(dates[1]):
                    # 计算出最大涨跌幅  (当天收盘价格-第一天收盘价格)/当天收盘价格
                    self.__compute__(queryset, results)
                else:
                    if datetime_util.string_2date(dates[1]) == date.today():
                        self.__compute__(queryset, results)
                    else:
                        self.__history_bUlk_add__(code, queryset[len(queryset) - 1].date)
                        queryset = list(IndexHistory.objects.filter(code=code, date__range=dates).order_by("date"))
                        self.__compute__(queryset, results)
        return SuccessResponse(results)

    def __compute__(self, queryset, results):
        logger.info(max(index.close for index in queryset))
        # 时间段
        high_period = 0
        low_period = 0
        high_date_start = 0
        high_date_end = 0
        low_date_start = 0
        low_date_end = 0
        fist_close = queryset[0].close
        high = max(queryset, key=lambda x: x.close)
        high_date_end = high.date
        low = min(queryset, key=lambda x: x.close)
        low_date_end = low.date
        # low = min(index.close for index in queryset)
        # 怎么求开始时间最大涨幅
        high_index = queryset.index(high)
        low_index = queryset.index(low)
        for i in range(high_index, -1, -1):
            index = queryset[i]
            if index.close <= fist_close:
                high_period = high_index - i
                high_date_start = index.date
                break
        for i in range(low_index, -1, -1):
            index = queryset[i]
            if index.close >= fist_close:
                low_period = low_index - i
                low_date_start = index.date
                break
        return results.append(
            {'code': queryset[0].code, 'name': queryset[0].name, 'fistClose': fist_close,
             'high': "%.2f" % (((high.close - fist_close) / fist_close) * 100),
             'highDate': high_date_start,
             'highDateEnd': high_date_end,
             'highPeriod': high_period,
             'low': "%.2f" % (((low.close - fist_close) / fist_close) * 100),
             'lowDate': low_date_start,
             'lowDateEnd': low_date_end,
             'lowPeriod': low_period})

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
                if date < x[0]:
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
