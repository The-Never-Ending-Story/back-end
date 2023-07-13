from django.http import JsonResponse
from .models import World
from .serializers import WorldSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .characters.models import Character
from .characters.serializers import CharacterSerializer
from .locations.models import Location
from .locations.serializers import LocationSerializer
from .events.models import Event
from .events.serializers import EventSerializer

@api_view(['GET', 'POST'])
def world_list(request):

  if request.method == 'GET':
    worlds = World.objects.all()
    serializer = WorldSerializer(worlds, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = WorldSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def world_detail(request, id):

  try:
    world = World.objects.get(pk=id)
  except World.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = WorldSerializer(world)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = WorldSerializer(world, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    world.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)

@api_view(['GET', 'POST'])
def character_list(request):

  if request.method == 'GET':
    characters = Character.objects.all()
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = CharacterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def character_detail(request, id):

  try:
    character = Character.objects.get(pk=id)
  except Character.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = CharacterSerializer(character)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CharacterSerializer(character, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    character.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)

@api_view(['GET', 'POST'])
def location_list(request):

  if request.method == 'GET':
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, id):

  try:
    location = Location.objects.get(pk=id)
  except Location.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = LocationSerializer(location)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = LocationSerializer(location, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    location.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)

@api_view(['GET', 'POST'])
def event_list(request):

  if request.method == 'GET':
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, id):

  try:
    event = Event.objects.get(pk=id)
  except Event.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = EventSerializer(event)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
      event.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    event.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)
  
@api_view(['GET', 'POST'])
def world_locations_list(request, id):

  if request.method == 'GET':
    world = World.objects.get(pk=id)
    locations = world.location_set.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def world_location_detail(request, world_id, id):

  try:
    world = World.objects.get(pk=world_id)
    locations = world.location_set.all()
    location = locations.get(pk=id)
  except World.DoesNotExist or Location.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == 'GET':
    serializer = LocationSerializer(location)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = LocationSerializer(location, data=request.data)
    if serializer.is_valid():
      location.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    location.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)
  
@api_view(['GET', 'POST'])
def world_characters_list(request, id):

  if request.method == 'GET':
    world = World.objects.get(pk=id)
    characters = world.character_set.all()
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = CharacterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def world_character_detail(request, world_id, id):

  try:
    world = World.objects.get(pk=world_id)
    characters = world.character_set.all()
    character = characters.get(pk=id)
  except World.DoesNotExist or Character.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == 'GET':
    serializer = CharacterSerializer(character)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CharacterSerializer(character, data=request.data)
    if serializer.is_valid():
      character.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    character.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)
  
@api_view(['GET', 'POST'])
def world_events_list(request, id):

  if request.method == 'GET':
    world = World.objects.get(pk=id)
    events = world.event_set.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)  
  elif request.method == 'POST':
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def world_event_detail(request, world_id, id):

  try:
    world = World.objects.get(pk=world_id)
    events = world.event_set.all()
    event = events.get(pk=id)
  except World.DoesNotExist or Event.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == 'GET':
    serializer = EventSerializer(event)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
      event.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    event.delete()
    return Response(status=status.HTTP_404_NO_CONTENT)