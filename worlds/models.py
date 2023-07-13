from django.db import models
from django.contrib.postgres.fields import ArrayField

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField(default=False)
    species = ArrayField(models.JSONField())
    geoDynamics = models.JSONField()
    magicTechnology = models.JSONField()
    img = ArrayField(models.TextField(default='none'), blank=True)
    history = ArrayField(models.TextField(default='none'))

    def __str__(self):
        return str(self.id) + " " + self.name