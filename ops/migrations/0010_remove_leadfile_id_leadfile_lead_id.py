# Generated by Django 4.1 on 2022-09-03 03:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0009_alter_leadfile_leads'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadfile',
            name='id',
        ),
        migrations.AddField(
            model_name='leadfile',
            name='lead_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
