from django.db import models

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField()
    species = models.JSONField()
    geoDynamics = models.JSONField()
    magicTechnology = models.JSONField()
    img = models.TextField(default='none')
    characters = models.JSONField(default=dict)
    locations = models.JSONField(default=dict)
    events = models.JSONField(default=dict)
    history = models.TextField(default=dict)

    def __str__(self):
        return str(self.id) + " " + self.name
