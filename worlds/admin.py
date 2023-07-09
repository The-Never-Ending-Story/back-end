from django.contrib import admin
from .models import World
from worlds.locations.models import Location

admin.site.register(World)
admin.site.register(Location)