import decimal
from apps.vadmin.stock.models.new_fund import NewFund
import akshare as ak

# 更新新发基金
from apps.vadmin.utils import datetime_util
from apps.vadmin.utils.decorators import BaseCeleryApp


@BaseCeleryApp(name='apps.vadmin.celery.tasks.update_new_fun')
def update_new_fun():
    fund = NewFund.objects.all().order_by("-date_establishment").first()
    dir_data = ak.fund_em_new_found().to_dict('records')
    daily_arr = []
    for x in dir_data:
        if datetime_util.string_2date(x['成立日期']) > fund.date_establishment:
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
            daily_arr.append(newfund)
    if daily_arr:
        NewFund.objects.bulk_create(daily_arr)
