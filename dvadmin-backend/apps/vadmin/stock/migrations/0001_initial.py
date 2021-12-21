# Generated by Django 2.2.16 on 2021-12-21 19:59

import apps.vadmin.op_drf.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='描述', null=True, verbose_name='描述')),
                ('modifier', apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='该记录最后修改者', max_length=255, null=True, verbose_name='修改者')),
                ('dept_belong_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='数据归属部门')),
                ('update_datetime', apps.vadmin.op_drf.fields.UpdateDateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', apps.vadmin.op_drf.fields.CreateDateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('code', models.CharField(max_length=64, verbose_name='代码')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('latest_price', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='最新价')),
                ('change_percent', models.DecimalField(decimal_places=3, max_digits=19, verbose_name='涨跌额')),
                ('price_change', models.DecimalField(decimal_places=3, max_digits=19, verbose_name='涨跌幅')),
                ('closed', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='昨收')),
                ('open', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='今开')),
                ('height', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='最高')),
                ('low', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='最低')),
                ('volume', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='成交量')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='成交额')),
                ('creator', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '指数数据',
                'verbose_name_plural': '指数数据',
            },
        ),
    ]
