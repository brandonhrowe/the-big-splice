from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.aggregates import Count
from random import randint

# Create your models here.
class FilmManager(models.Manager):
  def get_random_film(self):
    count = self.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    return self.all()[random_index]

class Film(models.Model):
  title = models.CharField(max_length=255)
  timecodes = ArrayField(models.CharField(max_length=10))
  runtime = models.CharField(max_length=10)
  tags = ArrayField(models.CharField(max_length=255, blank=True))
  collection = models.CharField(max_length=100)

  objects = models.Manager()
  random_film = FilmManager()

  def __str__(self):
    return self.title


