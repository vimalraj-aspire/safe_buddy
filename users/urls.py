from django.conf.urls import include, url
from django.contrib import admin

from views import  SBUserList, PasswordResetView, get_user, add_trackee, my_trackees, who_are_all_tracking_me


urlpatterns = [
    url(r'^users/$', SBUserList.as_view(), name='user-list'),
    url(r'^search-user/(?P<username>.*)/$', get_user, name='user-list'),
    url(r'^add-trackee/(?P<username>.*)/$', add_trackee, name='add-trackee'),
    url(r'^my-trackees/$', my_trackees, name='my-trackee'),
    url(r'^who-tracks-me/$', who_are_all_tracking_me, name='who-tracks-me'),
    url(r'^password-reset/$', PasswordResetView.as_view(), name='mobile_reset_password'),
]