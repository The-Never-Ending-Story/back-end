from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
          model = Event
          fields = ['id', 'description', 'world_id', 'location_id']