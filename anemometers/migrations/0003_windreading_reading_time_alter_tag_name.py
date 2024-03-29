# Generated by Django 4.1.5 on 2023-01-06 15:35

from django.db import migrations, models
import datetime
class Migration(migrations.Migration):

    dependencies = [
        ('anemometers', '0002_alter_anemometer_tags_windreading'),
    ]

    operations = [
        migrations.AddField(
            model_name='windreading',
            name='reading_time',
            field=models.DateTimeField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
