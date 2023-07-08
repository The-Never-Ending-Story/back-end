from django.http import JsonResponse
from .models import World
from .serializers import WorldSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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