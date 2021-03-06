from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from models import Location
from serializers import LocationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from users.serializers import SBUserSerializer
from models import Location
from users.models import Friend, EmployeeRole

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_location(request):
  ''' Function to update location'''
  request.data['user_profile'] = UserProfile.objects.get(user=request.user).id
  serializer = LocationSerializer(data=request.data)  
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_location(request, username):
  ''' Function to get location '''  
  locations = [{'user_first_name':location.user_profile.user.first_name, 'longitude': location.longitude, 'latitude':location.latitude , 'created_at': location.created_at,} for location in Location.objects.filter(user_profile=UserProfile.objects.get(user__username=username)).order_by('created_at')][-5:]
  return Response(locations)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_my_trackees_location(request):
  ''' Function to get location '''
  friends = Friend.objects.filter(user_profile=UserProfile.objects.get(user=request.user))
  friends_location = []
  for friend in friends.values('friend_profile'):    
    locations = [{'user_first_name':location.user_profile.user.first_name, 'longitude': location.longitude, 'latitude':location.latitude , 'created_at': location.created_at,} for location in Location.objects.filter(user_profile=UserProfile.objects.get(id=friend.get('friend_profile'))).order_by('created_at')][-5:]
    friends_location.append(locations)
  return Response(friends_location)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_employees_location_by_department(request, department_id):
  ''' Function to get location '''
  friends = EmployeeRole.objects.filter(department=department_id).values('employee')
  friends_location = []
  for friend in friends:
    locations = [{'user_first_name':location.user_profile.user.first_name, 'longitude': location.longitude, 'latitude':location.latitude , 'created_at': location.created_at,} for location in Location.objects.filter(user_profile=UserProfile.objects.get(id=friend.get('employee'))).order_by('created_at')][-5:]
    if len(locations):
      friends_location.append(locations)
  return Response(friends_location)