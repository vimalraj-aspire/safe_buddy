from rest_framework import serializers

from django.contrib.auth.models import User


class SBUserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ('id', 'password', 'first_name', 'last_name', 'email', 'username')
    extra_kwargs = {'password': {'write_only': True}}
    readonly_fields = ('is_active', 'date_joined')

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()
    return user
