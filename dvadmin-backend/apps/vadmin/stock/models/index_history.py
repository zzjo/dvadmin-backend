from django.db.models import CharField, DecimalField, DateField

from apps.vadmin.op_drf.models import CoreModel


class IndexHistory(CoreModel):
    name = CharField(max_length=64, verbose_name="名称")
    code = CharField(max_length=64, verbose_name="代码")
    date = DateField(verbose_name="时间")
    open = DecimalField(max_digits=19, decimal_places=3, verbose_name="开盘价")
    high = DecimalField(max_digits=19, decimal_places=3, verbose_name="最高价")
    low = DecimalField(max_digits=19, decimal_places=3, verbose_name="最低价")
    close = DecimalField(max_digits=19, decimal_places=3, verbose_name="收盘价")
    volume = DecimalField(max_digits=19, decimal_places=0, verbose_name="成交量")

    class Meta:
        verbose_name = "指数历史数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
