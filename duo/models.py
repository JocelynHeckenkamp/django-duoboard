from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    streak = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    lingots = models.IntegerField(default=0)
    def __str__(self):
        return self.username

class Username(models.Model):
    username = models.CharField(max_length=255)
    def __str__(self):
        return self.username
