from django.db import models
from dateti import dateTime

class User(models.Model):
    user_id = models.IntegerField(blank = True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    creation_date  models.DateTimeField(default=datetime.now, blank = True)


