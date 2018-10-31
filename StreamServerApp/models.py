from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=100)
    baseurl = models.CharField(max_length=100, default="")
