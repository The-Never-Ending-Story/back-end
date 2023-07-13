from rest_framework import serializers
from .models import World

from .characters.models import Character
from .characters.serializers import CharacterSerializer
from .locations.models import Location
from .locations.serializers import LocationSerializer
from .events.models import Event
from .events.serializers import EventSerializer

class WorldSerializer(serializers.ModelSerializer):
    characters = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()

    class Meta:
        model = World
        fields = ['id', 'name', 'blurb', 'description', 'discovered', 'species', 'geodynamics', 'magictechnology', 'img', 'characters', 'locations', 'events', 'history' ]

    def get_characters(self, obj):
        characters = Character.objects.filter(world=obj)
        serializer = CharacterSerializer(characters, many=True)
        return serializer.data

    def get_locations(self, obj):
        locations = Location.objects.filter(world=obj)
        serializer = LocationSerializer(locations, many=True)
        return serializer.data

    def get_events(self, obj):
        events = Event.objects.filter(world=obj)
        serializer = EventSerializer(events, many=True)
        return serializer.data
