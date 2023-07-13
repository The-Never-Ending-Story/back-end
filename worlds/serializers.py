from rest_framework import serializers
from .models import World
from .locations.serializers import LocationSerializer
from .characters.serializers import CharacterSerializer
from .events.serializers import EventSerializer

class WorldSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    characters = CharacterSerializer(many=True)
    events = EventSerializer(many=True)

    class Meta:
          model = World
          fields = ['id', 'name', 'blurb', 'description', 'species', 'geodynamics', 'magicTechnology', 'img', 'locations', 'characters', 'events', 'history' ]

