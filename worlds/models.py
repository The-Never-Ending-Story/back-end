from django.db import models
from species.models import Species
from events.models import Event
from locations.models import Location
from characters.models import Character

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
    img = models.JSONField(default={"thumbnail": "", "landscape": ""})
    imgs = models.JSONField(default={"thumbnails": [], "landscapes": []})
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
