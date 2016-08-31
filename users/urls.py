from django.conf.urls import include, url
from django.contrib import admin

from .views import  SBUserList



urlpatterns = [
    url(r'^users/$', SBUserList.as_view(), name='user-list'),
]