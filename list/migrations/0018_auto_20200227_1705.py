# Generated by Django 2.2.10 on 2020-02-27 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0017_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]