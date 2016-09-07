from rest_framework import serializers
from models import Location
from users.serializers import SBUserSerializer

class LocationSerializer(serializers.ModelSerializer):
  # user_profile = SBUserSerializer()
  class Meta:
    model = Location
    fields = ('latitude', 'longitude', 'created_at', 'user_profile')
    readonly_fields = ('created_at')

  def to_representation(self, obj):
    output = {}
    output['latitude'] = obj.latitude
    output['longitude'] = obj.latitude
    output['created_at'] = obj.latitude
    output['user'] = obj.user_profile.user.username
    return output

