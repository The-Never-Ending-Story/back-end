from django.db import models
from species.models import Species
from events.models import Event
from locations.models import Location
from characters.models import Character

class World(models.Model):
    name = models.CharField(max_length=250)
    discovered = models.BooleanField(default=False)
    earthly = models.BooleanField()
    genres = models.JSONField()
    blurb = models.CharField(max_length=250)
    description = models.TextField()
    geoDynamics = models.JSONField()
    magicTechnology = models.JSONField()
    imagine = models.TextField(default='')
    img = models.TextField(default='')
    lore = models.JSONField(default=list)


    @property
    def locations(self):
        return self.location_set.all()

    @property
    def characters(self):
        return self.character_set.all()
    
    @property
    def events(self):
        return self.event_set.all()
    
    @property
    def species(self):
        return self.species_set.all()
    
    def __str__(self):
        return str(self.id) + " " + self.name
