from apps.vadmin.monitor.models import Server, Monitor
from apps.vadmin.op_drf.serializers import CustomModelSerializer

# ================================================= #
# ************** 指数数据 序列化器  ************** #
# ================================================= #
from apps.vadmin.stock.models import Index, NewFund, IndexHistory


class NewFundSerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = NewFund
        fields = '__all__'


class IndexHistorySerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = IndexHistory
        fields = '__all__'


class IndexSerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = Index
        fields = '__all__'
