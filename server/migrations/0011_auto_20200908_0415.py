# Generated by Django 3.0.6 on 2020-09-08 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_optionalshares_name_cn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionalshares',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
