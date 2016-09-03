from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contact(models.Model):  
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)

    def __unicode__(self):
      return self.name

class SafetyTip(models.Model):
  text = models.CharField(max_length=300)  
  image = models.ImageField(upload_to='static/safety_image/', blank=False)

  def __unicode__(self):
      return self.text