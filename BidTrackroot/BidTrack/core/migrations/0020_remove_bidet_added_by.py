# Generated by Django 5.0.7 on 2024-07-17 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_bidet_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidet',
            name='added_by',
        ),
    ]
