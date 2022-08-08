from django.db import models


class WarningHistory(models.Model):
    type = models.IntegerField(verbose_name='类型')
    bigImg = models.FileField(upload_to='warning/', verbose_name='大图')
    imgBase = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class PushUser(models.Model):
    name = models.CharField(max_length=10)
    enable = models.BooleanField(default=True)
    phone = models.IntegerField()


class Environmental(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    la = models.FloatField()
