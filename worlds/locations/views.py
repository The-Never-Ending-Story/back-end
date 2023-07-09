from django.http import JsonResponse
from .models import Location
from .serializers import LocationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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