# Generated by Django 5.0.7 on 2024-07-19 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_bidet_closing_time_alter_bidet_opening_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidet',
            name='address',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='bidet',
            name='closing_time',
            field=models.TimeField(default=datetime.time(23, 59)),
        ),
        migrations.AlterField(
            model_name='bidet',
            name='opening_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]