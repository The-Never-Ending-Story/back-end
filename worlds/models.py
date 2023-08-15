from django.db import models
from species.models import Species
from events.models import Event
from locations.models import Location
from characters.models import Character
import re

class World(models.Model):
    name = models.CharField(max_length=250)
    discovered = models.BooleanField(default=False)
    earthly = models.BooleanField(default=True)
    genres = models.JSONField(default=dict)
    blurb = models.CharField(max_length=250)
    description = models.TextField(default='')
    geoDynamics = models.JSONField(default=dict)
    magicTechnology = models.JSONField(default=dict)
    imagine = models.TextField(default='')
    img = models.JSONField(default=dict)
    imgs = models.JSONField(default=dict)
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
    
    @property
    def is_complete(self):
        pattern = re.compile(r"\.png$")
        
        if not (self.img["thumbnail"] and self.img["landscape"] and pattern.search(self.img["thumbnail"]) and pattern.search(self.img["landscape"])):
            return False
        
        for model in [self.locations, self.events, self.characters, self.species]:
            for instance in model:
                if not instance.img and pattern.search(instance.img):
                    return False
        
        return True

    def __str__(self):
        return str(self.id) + " " + self.name
