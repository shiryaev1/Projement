# Generated by Django 2.2 on 2019-12-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20191205_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyofchanges',
            name='additional_hour_design',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='additional_hour_development',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='additional_hour_testing',
            field=models.CharField(blank=True, max_length=164),
        ),
    ]