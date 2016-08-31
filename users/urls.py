from django.conf.urls import include, url
from django.contrib import admin

from .views import  SBUserList, PasswordResetView



urlpatterns = [
    url(r'^users/$', SBUserList.as_view(), name='user-list'),
    url(r'^password-reset/$', PasswordResetView.as_view(), name='mobile_reset_password'),
]