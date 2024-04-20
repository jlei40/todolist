from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField()

    class Meta:
        ordering = ['name']
