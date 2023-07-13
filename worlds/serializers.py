from rest_framework import serializers
from .models import World

class WorldSerializer(serializers.ModelSerializer):

    class Meta:
        model = World
        fields = ['id', 'name', 'blurb', 'description', 'discovered', 'species', 'geoDynamics', 'magicTechnology', 'img', 'characters', 'locations', 'events', 'history' ]
