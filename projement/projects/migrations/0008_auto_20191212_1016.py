# Generated by Django 2.2 on 2019-12-12 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20191211_0533'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataOfTag',
            new_name='TagAddingHistory',
        ),
    ]
