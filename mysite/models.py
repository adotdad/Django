from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contractor = models.BooleanField


class Job(models.Model):
    title = models.CharField(max_length=50)
    value = models.IntegerField(max_length=15)
    approx_time = models.IntegerField(max_length=6)
    employer = models.CharField(max_length=50)

