# Generated by Django 2.2.10 on 2020-02-27 08:54

from django.db import migrations, models
import list.models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0016_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
