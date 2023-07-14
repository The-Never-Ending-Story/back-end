from django.db import models

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField(default=False)
    species = models.JSONField(default=dict)
    geoDynamics = models.JSONField(default=dict)
    magicTechnology = models.JSONField(default=dict)
    img = models.TextField(default='none')
    history = models.TextField(default=dict)

    def __str__(self):
        return str(self.id) + " " + self.name
