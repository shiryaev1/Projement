# Generated by Django 2.2 on 2019-12-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
