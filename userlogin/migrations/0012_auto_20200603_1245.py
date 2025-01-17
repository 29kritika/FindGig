# Generated by Django 2.2.12 on 2020-06-03 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0011_event_sponsors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsors',
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.PositiveSmallIntegerField(default=0)),
                ('Event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='userlogin.Event')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor', to='userlogin.User')),
            ],
        ),
    ]
