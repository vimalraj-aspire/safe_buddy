from django.conf.urls import include, url
from django.contrib import admin
from views import update_location, get_location, get_my_trackees_location, get_employees_location_by_department

urlpatterns = [
    url(r'^update-location/$', update_location, name='update-location'),
    url(r'^get-location/(?P<username>.*)/$', get_location, name='update-location'),
    url(r'^get-my-trackees-location/$', get_my_trackees_location, name='get-my-trackees-location'),
    url(r'^get-employees-location-by-department/(?P<department_id>.*)/$', get_employees_location_by_department, name='get-employees-location-by-department'),
    ]