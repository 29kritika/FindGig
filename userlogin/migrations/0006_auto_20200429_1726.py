# Generated by Django 2.2.12 on 2020-04-29 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0005_auto_20200427_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about_link',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other'), ('not specified', 'Not specified')], default='Not specified', max_length=20),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2500)),
                ('venue', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('dateTime', models.DateTimeField(auto_now=True)),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Organiser', to='userlogin.User')),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Performer', to='userlogin.User')),
            ],
        ),
    ]
