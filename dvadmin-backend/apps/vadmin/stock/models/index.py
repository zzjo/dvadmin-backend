from django.db.models import CharField, DecimalField

from apps.vadmin.op_drf.models import CoreModel


class Index(CoreModel):
    code = CharField(max_length=64, verbose_name="代码")
    name = CharField(max_length=64, verbose_name="名称")
    latest_price = DecimalField(max_digits=19, decimal_places=4, verbose_name="最新价")
    change_percent = DecimalField(max_digits=19, decimal_places=3, verbose_name="涨跌额")
    price_change = DecimalField(max_digits=19, decimal_places=3, verbose_name="涨跌幅")
    closed = DecimalField(max_digits=19, decimal_places=4, verbose_name="昨收")
    open = DecimalField(max_digits=19, decimal_places=4, verbose_name="今开")
    height = DecimalField(max_digits=19, decimal_places=4, verbose_name="最高")
    low = DecimalField(max_digits=19, decimal_places=4, verbose_name="最低")
    volume = DecimalField(max_digits=19, decimal_places=4, verbose_name="成交量")
    amount = DecimalField(max_digits=19, decimal_places=4, verbose_name="成交额")

    class Meta:
        verbose_name = "指数数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
