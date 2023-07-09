from django.contrib import admin
from .models import World
from worlds.locations.models import Location
from worlds.characters.models import Character

admin.site.register(World)
admin.site.register(Location)
admin.site.register(Character)