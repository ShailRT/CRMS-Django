# Generated by Django 4.1 on 2022-09-03 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0005_leadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadfile',
            name='leads',
            field=models.CharField(max_length=500),
        ),
    ]
