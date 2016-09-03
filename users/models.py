from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):  
    user = models.OneToOneField(User, unique=True)
    aceid = models.CharField(max_length=10)  
    profile_picture = models.ImageField(upload_to='static/thumbpath', blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username