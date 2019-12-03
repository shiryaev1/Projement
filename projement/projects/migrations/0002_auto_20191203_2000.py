# Generated by Django 2.2 on 2019-12-03 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyofchanges',
            old_name='actual_development',
            new_name='change_delta_actual_design',
        ),
        migrations.RenameField(
            model_name='historyofchanges',
            old_name='actual_testing',
            new_name='change_delta_actual_development',
        ),
        migrations.RenameField(
            model_name='historyofchanges',
            old_name='change_actual_design',
            new_name='change_delta_actual_testing',
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='initial_actual_design',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='initial_actual_development',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='initial_actual_testing',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='resulting_actual_design',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='resulting_actual_development',
            field=models.CharField(blank=True, max_length=164),
        ),
        migrations.AddField(
            model_name='historyofchanges',
            name='resulting_actual_testing',
            field=models.CharField(blank=True, max_length=164),
        ),
    ]
