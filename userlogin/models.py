from djongo import models
from embed_video.fields import EmbedVideoField

# Create your models here.
from django.contrib.auth.models import User as djangoUser


class User(models.Model):
    user = models.OneToOneField(djangoUser, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
    type = models.TextField(max_length=500, choices=(('artist', 'Artist'), ('organiser', 'Organiser'), ('band', 'Band'),
                                                     ('custom user', 'Custom User')), default='artist')
    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    about_text = models.CharField(max_length=500, default='')
    about_link = models.CharField(max_length=50, default='-')
    gender = models.CharField(max_length=20, default='Not specified', choices=(
    ('female', 'Female'), ('male', 'Male'), ('other', 'Other'), ('not specified', 'Not specified')))
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
    video = EmbedVideoField(default='')
    calendar_link = models.CharField(max_length=500, default='')


class Sponsor(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsor')
    Amount = models.PositiveSmallIntegerField(default=0)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sponsor_event')


class Post(models.Model):
    dateTime = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2500)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='post_user')
    video = EmbedVideoField(default='')


class Performer(models.Model):
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performer')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='performance_event')
    request_accepted = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)


class RatedPost(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewer2')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post2')
    liked = models.BooleanField(default=True)
