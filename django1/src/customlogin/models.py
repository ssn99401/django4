from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    point=models.IntegerField(default=0,blank=True)
    latitude = models.IntegerField(default=0,blank=True)
    longitude = models.IntegerField(default=0,blank=True)