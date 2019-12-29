# Generated by Django 2.0 on 2019-12-28 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20191228_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='projects.Company'),
        ),
    ]
