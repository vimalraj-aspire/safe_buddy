from django.shortcuts import render
from .serializers import SBUserSerializer, PasswordResetSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from serializers import UserSerializer
from models import UserProfile
from rest_framework.request import Request
from safe_buddy import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_user(request, username):
  ''' Function to user detail '''
  try:
    user = UserProfile.objects.filter(user__username=username)
    serializer = SBUserSerializer(user, many=True)
    return Response(serializer.data)
  except UserProfile.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('USER_DOES_NOT_EXISTS')}, status=status.HTTP_403_FORBIDDEN)



class SBUserList(APIView):
    """
    List all SB users, or create a new SB user.
    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        user = UserProfile.objects.all().exclude(user__is_superuser=1)
        serializer = SBUserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer_context = {
        'request': Request(request),
        }

        user_data = {}
        user_data['email'] = request.data.pop('email')[0]
        user_data['username'] = request.data.pop('username')[0]
        user_data['password'] = request.data.pop('password')[0]
        user_data['first_name'] = request.data.pop('first_name')[0]

        user_seriliazer = UserSerializer(data=user_data)
        if user_seriliazer.is_valid(request.data):
            user  = user_seriliazer.save()
            request.data['user'] = user.id
            serializer = SBUserSerializer(data=request.data, context=serializer_context)
            if serializer.is_valid():
                employee = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST.get('email',''))
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True})
        else:
            return Response(
                {"failed": serializer.errors},
                status=400
            )