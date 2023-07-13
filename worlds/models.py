from django.db import models

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField()
    species = models.JSONField(default=dict)
    geodynamics = models.JSONField(default=dict)
    magictechnology = models.JSONField(default=dict)
    img = models.TextField(default='none')
    history = models.TextField(default='none')

    def __str__(self):
        return str(self.id) + " " + self.name