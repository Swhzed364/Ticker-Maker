from django.db import models
from django.utils import timezone

class Ticker(models.Model):
    video = models.CharField()
    creation_date = models.DateTimeField(auto_now_add=True)