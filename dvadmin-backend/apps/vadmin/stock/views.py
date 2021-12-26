import logging
from datetime import datetime

from rest_framework.request import Request
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.stock.models.index import Index
from apps.vadmin.stock.models.index_history import IndexHistory
from apps.vadmin.stock.serializers import IndexHistorySerializer, IndexSerializer
import akshare as ak
import numpy as np

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class IndexHistoryModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = IndexHistory.objects.all()
    serializer_class = IndexHistorySerializer

    # 获取某时间段的涨幅
    def get_time_period(self, request: Request, *args, **kwargs):
        # 循环指数

        # 指数是否为空
        queryset = IndexHistory.objects.filter(name__in=kwargs.get("ids"))
        if queryset.exists():
            pass
        else:
            ak.stock_zh_index_daily(symbol="sz399552")

    class IndexModelViewSet(CustomModelViewSet):
        """
        菜单模型 的CRUD视图
        """
        queryset = Index.objects.all()
        serializer_class = IndexSerializer

        # 查询指数名称
        def get_index_list(self, request: Request, *args, **kwargs):
            namelist = Index.objects.values("name")
            return SuccessResponse([item[key] for item in namelist for key in item])

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
