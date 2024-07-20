from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_bidet_handicap_friendly'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidet',
            name='closing_time',
            field=models.TimeField(),
        ),
        migrations.AddField(
            model_name='bidet',
            name='opening_time',
            field=models.TimeField(),
        ),
    ]
