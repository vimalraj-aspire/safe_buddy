from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True)
    aceid = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='static/thumbpath', blank=True)
    user_relation = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Friend(models.Model):
  user_profile =  models.ForeignKey(UserProfile, blank=False, null=True, on_delete=models.SET_NULL, default=None, related_name='userprofile')
  friend_profile =  models.ForeignKey(UserProfile, blank=False, null=True, on_delete=models.SET_NULL, default=None,related_name='friendprofile')

class Department(models.Model):
 name = models.CharField(max_length=30)

class EmployeeRole(models.Model):
  '''
    Employee role model, an employee can be a partr of multiple teams 
  '''
  employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)
  role = models.IntegerField(default=2)

class EmergencyContact(models.Model):
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    number = models.CharField(max_length=10)