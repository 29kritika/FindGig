# Generated by Django 2.2.12 on 2020-04-29 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0006_auto_20200429_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='dateTime',
        ),
    ]