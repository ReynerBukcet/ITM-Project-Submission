# Generated by Django 5.0.7 on 2024-07-16 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_bidet_slug_alter_bidet_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidet',
            name='slug',
        ),
    ]