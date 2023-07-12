from django.db import models

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField()
    species = models.JSONField()
    geodynamics = models.JSONField()
    magictechnology = models.JSONField()
    img = models.TextField(default='none')
    characters = models.JSONField(default='none')
    locations = models.JSONField(default='none')
    events = models.JSONField(default='none')
    history = models.TextField(default='none')

    def __str__(self):
        return str(self.id) + " " + self.name