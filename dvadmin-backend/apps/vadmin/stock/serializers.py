from apps.vadmin.monitor.models import Server, Monitor
from apps.vadmin.op_drf.serializers import CustomModelSerializer


# ================================================= #
# ************** 指数数据 序列化器  ************** #
# ================================================= #
from apps.vadmin.stock.models import Index


class IndexSerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = Index
        fields = '__all__'