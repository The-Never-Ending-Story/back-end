from django.contrib import admin
from .models import World
from worlds.locations.models import Location
from worlds.characters.models import Character
from worlds.events.models import Event

admin.site.register(World)
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Event)