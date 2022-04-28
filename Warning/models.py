from django.db import models


class WarningHistory(models.Model):
    imgBase = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class PushUser(models.Model):
    name = models.CharField(max_length=10)
    phone = models.IntegerField()


