from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from safe_buddy import settings

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
