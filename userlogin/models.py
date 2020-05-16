from djongo import models
from embed_video.fields import EmbedVideoField

# Create your models here.
from django.contrib.auth.models import User as djangoUser


class User(models.Model):
    user = models.OneToOneField(djangoUser, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
    type = models.TextField(max_length=500, choices=(('artist', 'Artist'), ('organiser', 'Organiser'), ('band', 'Band')),
                            default='artist')
    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    about_text = models.CharField(max_length=500, default='')
    about_link = models.CharField(max_length=50, default='-')
    gender = models.CharField(max_length=20, default='Not specified', choices=(('female', 'Female'), ('male', 'Male'), ('other', 'Other'), ('not specified', 'Not specified')))
    city = models.CharField(max_length=50, default='')
    USERNAME_FIELD = 'username'


class Event(models.Model):
    organiser = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Organiser")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2500)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Performer")
    video = EmbedVideoField(default='')
    # sponsorramt = models.PositiveINtegerField(default=0)
    sponsor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Sponsor")
    # dateTime = models.DateTimeField(auto_now=True) not able to get this value


class Post(models.Model):
    dateTime = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2500)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='post_user')
    video = EmbedVideoField(default='')


# class Song(models.Model):
#     id = models.TextField(max_length=10, unique=True, null=False, db_index=True)
#     name = models.TextField(max_length=200, null=False)
#     Genre = models.TextField(max_length=200, null=False)
#
#
# class Relation(models.Model):
#     singer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     song_sang = models.ForeignKey(Song, on_delete=models.CASCADE)
#
# class Timeline(models.Model):
#     from_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_t1")
#     to_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_t2")
#     post = models.CharField(max_length=2500)
#     datetime = models.DateTimeField(auto_now=True)
#     privacy = models.BooleanField(default=False)
#     selfp = models.BooleanField(default=True)