from django.db.models import CharField, DateField, DecimalField

from apps.vadmin.op_drf.models import CoreModel


class NewFund(CoreModel):
    name = CharField(max_length=64, verbose_name="基金简称")
    code = CharField(max_length=64, verbose_name="基金代码")
    publisher = CharField(max_length=64, verbose_name="发行公司")
    fund_type = CharField(max_length=64, verbose_name="基金类型")
    subscription_period = CharField(max_length=64, verbose_name="集中认购期")
    raise_shares = DecimalField(max_digits=19, decimal_places=3, verbose_name="募集份额")
    date_establishment = DateField(verbose_name="成立日期")
    established_increase = DecimalField(max_digits=19, decimal_places=3, verbose_name="成立来涨幅")
    fund_manager = CharField(max_length=64, verbose_name="基金经理")
    subscription_status = CharField(max_length=64, verbose_name="申购状态")
    discount_rate = CharField(max_length=64, verbose_name="优惠费率")

    class Meta:
        verbose_name = "新发布公墓基金"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
