# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-16 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.IntegerField()),
                ('goods', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=50)),
                ('descr', models.TextField()),
                ('price', models.FloatField()),
                ('picname', models.CharField(max_length=255)),
                ('state', models.IntegerField(default=1)),
                ('store', models.IntegerField(default=0)),
                ('num', models.IntegerField(default=0)),
                ('clicknum', models.IntegerField(default=0)),
                ('addtime', models.IntegerField()),
            ],
            options={
                'db_table': 'goods_info',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.GoodsInfo')),
            ],
            options={
                'db_table': 'orderdetailinfo',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('odate', models.DateTimeField(auto_now=True)),
                ('oIspay', models.BooleanField(default=False)),
                ('ptotal', models.DecimalField(decimal_places=2, max_digits=6)),
                ('orecive', models.CharField(max_length=5)),
                ('oaddress', models.CharField(max_length=29)),
                ('ophone', models.CharField(default='', max_length=11)),
                ('oyoubian', models.CharField(default='', max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.UserInfo')),
            ],
            options={
                'db_table': 'orderinfo',
            },
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.OrderInfo'),
        ),
    ]
