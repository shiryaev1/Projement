# Generated by Django 2.2 on 2019-12-11 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20191210_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, default=None, related_name='project', to='projects.Tag'),
        ),
    ]