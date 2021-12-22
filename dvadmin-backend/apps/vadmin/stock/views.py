from datetime import datetime

from rest_framework.request import Request

from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.stock.models.index import Index
from apps.vadmin.stock.serializers import IndexSerializer
import akshare as ak
import numpy as np


class IndexModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

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
