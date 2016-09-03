from django.shortcuts import render
from serializers import ContactSerializer, SafetyTipsSerializer
from models import Contact, SafetyTip
from rest_framework import viewsets


class ContactViewSet(viewsets.ModelViewSet):
  serializer_class = ContactSerializer
  queryset = Contact.objects.all()


class SafetyTipsViewSet(viewsets.ModelViewSet):
  serializer_class = SafetyTipsSerializer
  queryset = SafetyTip.objects.all()