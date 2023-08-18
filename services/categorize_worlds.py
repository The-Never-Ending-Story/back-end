from .attributes import categorize_world, CATEGORIES
from worlds.models import World

worlds = World.objects.all()
for world in worlds:
    categorize_world(world)