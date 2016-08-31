from django.shortcuts import render
from .serializers import SBUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status


class SBUserList(APIView):
    """
    List all SB users, or create a new SB user.
    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        user = User.objects.all().exclude(is_superuser=1)
        serializer = SBUserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SBUserSerializer(data=request.data)
        if serializer.is_valid(request.data):
            employee = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
