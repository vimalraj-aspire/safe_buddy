from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from models import UserProfile, Friend
from safe_buddy import settings
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'password', 'first_name',  'email', 'username')
    extra_kwargs = {'password': {'write_only': True}}
    readonly_fields = ('is_active', 'date_joined')

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()
    return user

class SBUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = UserProfile
    fields = ('aceid', 'profile_picture', 'user', 'user_relation', 'user_type')
    user = serializers.Field(source='user.id')

  def to_representation(self, instance):
      data = super(SBUserSerializer, self).to_representation(instance)
      data['first_name'] = instance.user.first_name
      data['email'] = instance.user.email
      data['username'] = instance.user.username
      if data['profile_picture'] and 'http' in data['profile_picture']:
        data['profile_picture'] = '/'.join(data['profile_picture'].split('/')[5:])
      data.pop('user')
      return data
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def is_valid(self):
        self._errors = {}
        self.reset_form = self.password_reset_form_class(data={'email':self.initial_data})
        if not self.reset_form.is_valid():
            self._errors['fields'] = self.reset_form.errors
            return
        return True

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
        }
        self.reset_form.save(**opts)



class FriendSertializer(serializers.ModelSerializer):
  friend_profile = SBUserSerializer()
  class Meta:
    model = Friend
    fields = ('friend_profile',)
