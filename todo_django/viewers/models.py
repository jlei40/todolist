from django.db import models


# Create your models here.

class Viewer(models.Model):
    name = models.CharField(max_length=200, unique=True)