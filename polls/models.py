from django.contrib.auth.models import User
from django.db import models
import datetime


class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contractor = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class AssignedJobs(models.Model):
    job = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.job


class Job(models.Model):
    title = models.CharField(max_length=50)
    value = models.IntegerField()
    approx_time = models.IntegerField()
    employer = models.CharField(max_length=50)
    date = models.TimeField(default=datetime.datetime(2016, 9, 30))
    description = models.CharField(max_length=500)
    assigned_user = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

