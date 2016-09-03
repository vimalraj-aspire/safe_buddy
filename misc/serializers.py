from rest_framework import serializers
from models import Contact, SafetyTip

class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contact



class SafetyTipsSerializer(serializers.ModelSerializer):
  class Meta:
    model = SafetyTip


  def to_representation(self, instance):
      data = super(SafetyTipsSerializer, self).to_representation(instance)
      if 'http' in data['image']:
        data['image'] = '/'.join(data['image'].split('/')[4:])
      return data
