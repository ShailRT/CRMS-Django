# Generated by Django 4.1 on 2022-12-10 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0016_heap_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leadfile',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='heap',
            name='date_created',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
