import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Update with your actual settings module

import django
django.setup()

from .attributes import categorize_world, CATEGORIES
from worlds.models import World

worlds = World.objects.all()
for world in worlds:
    categorize_world(world)