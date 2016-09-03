from django.conf.urls import include, url
from django.contrib import admin
from views import ContactViewSet, SafetyTipsViewSet

contact_list = ContactViewSet.as_view({
    'get': 'list',
})

safety_tip_list = SafetyTipsViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    url(r'^misc-contacts/$', contact_list, name='contact-list'),
    url(r'^safety-tips/$', safety_tip_list, name='safety-tip-list'),
]
