from __future__ import unicode_literals
from users.models import UserProfile
from django.db import models
from datetime import datetime

class Location(models.Model):
  user_profile =  models.ForeignKey(UserProfile, blank=False, null=True, on_delete=models.SET_NULL, default=None, related_name='userprofileLocation')
  latitude = models.DecimalField(max_digits=8, decimal_places=6)
  longitude = models.DecimalField(max_digits=8, decimal_places=6)
  created_at = models.DateTimeField(default=datetime.now)
  