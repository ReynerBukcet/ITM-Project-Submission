# Generated by Django 5.0.7 on 2024-07-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_bidet_water_strength'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidet',
            name='water_strength',
        ),
        migrations.AlterField(
            model_name='bidet',
            name='address',
            field=models.CharField(max_length=1000000),
        ),
    ]
