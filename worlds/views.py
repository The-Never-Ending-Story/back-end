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