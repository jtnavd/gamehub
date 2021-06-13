from django.db import models
from datetime import datetime


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(default=datetime.now, blank = True)


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    creation_date = models.DateTimeField(default=datetime.now, blank = True)
    steam_id = models.CharField(max_length=200)

class Game(models.Model):
    steam_id = models.ManyToManyField(Profile)
    game_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(default=datetime.now, blank = True)

