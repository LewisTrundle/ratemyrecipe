# Generated by Django 2.2.17 on 2021-03-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratemyrecipeapp', '0003_auto_20210312_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_needed',
            field=models.DurationField(help_text='HH:MM:SS format'),
        ),
    ]