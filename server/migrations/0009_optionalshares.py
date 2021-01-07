# Generated by Django 3.0.6 on 2020-09-07 17:19

from django.db import migrations, models
import server.verification


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_financialanalytical_operation_cash_flow_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionalShares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_created=True)),
                ('stock_code', models.CharField(default='123456', max_length=255, verbose_name='股票代码')),
                ('exchange', models.CharField(default='SZ', max_length=8, verbose_name='所属交易所')),
                ('user_code', models.CharField(default=server.verification.create_16_code, max_length=255, unique=True, verbose_name='用户编号')),
            ],
        ),
    ]
