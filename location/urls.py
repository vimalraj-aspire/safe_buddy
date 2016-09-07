from django.conf.urls import include, url
from django.contrib import admin
from views import update_location, get_location

urlpatterns = [
    url(r'^update-location/$', update_location, name='update-location'),
    url(r'^get-location/(?P<username>.*)/$', get_location, name='update-location'),
    ]