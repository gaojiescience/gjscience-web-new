# Generated by Django 3.0.6 on 2020-09-01 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20200828_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialanalytical',
            name='operation_cash_flow_ratio',
            field=models.CharField(default='123456', max_length=255, verbose_name='现金流量比率'),
        ),
    ]
