# Generated by Django 2.0 on 2019-12-13 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20191213_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialdataofproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]