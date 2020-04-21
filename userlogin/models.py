from djongo import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
    type = models.TextField(max_length=500, blank=True)


# class Song(models.Model):
#     id = models.TextField(max_length=10, unique=True, null=False, db_index=True)
#     name = models.TextField(max_length=200, null=False)
#     Genre = models.TextField(max_length=200, null=False)
#
#
# class Relation(models.Model):
#     singer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     song_sang = models.ForeignKey(Song, on_delete=models.CASCADE)
