from django.db import models

class World(models.Model):
    name = models.CharField(max_length=250)
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    discovered = models.BooleanField()
    species = models.JSONField()
    geodynamics = models.JSONField()
    magicTechnology = models.JSONField()
    img = models.TextField(default='none')
    history = models.TextField(default=dict)

    @property
    def locations(self):
        return self.location_set.all()

    @property
    def characters(self):
        return self.character_set.all()
    
    @property
    def events(self):
        return self.event_set.all()
    
    def __str__(self):
        return str(self.id) + " " + self.name