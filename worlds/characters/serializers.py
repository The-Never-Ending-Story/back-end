from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
          model = Character
          fields = ['id', 'name', 'race', 'alignment', 'attributes', 'description', 'img', 'world_id', 'location_id']