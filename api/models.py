from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.aggregates import Count
from random import randint

# Create your models here.
class FilmManager(models.Manager):
  def get_random_film(self):
    count = self.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    return self.all().values()[random_index]

class Film(models.Model):
  title = models.CharField(max_length=255)
  identifier = models.CharField(max_length=255)
  timecodes = ArrayField(models.CharField(max_length=100))
  url = models.URLField()
  file_name = models.CharField(max_length=100)
  tags = ArrayField(models.CharField(max_length=255, blank=True))
  collection = ArrayField(models.CharField(max_length=100))
  description = models.TextField(blank=True)
  resolution_width = models.IntegerField(default=0)
  resolution_height = models.IntegerField(default=0)
  frame_rate = models.CharField(max_length=100)
  duration = models.CharField(max_length=100)

  objects = models.Manager()
  random_film = FilmManager()

  def __str__(self):
    return self.title


