from django.conf.urls import include, url
from django.contrib import admin

from views import  SBUserList, DepartmentViewSet, PasswordResetView, get_user, add_trackee, my_trackees, who_are_all_tracking_me, map_employee, get_employees_by_department


department_list = DepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    url(r'^users/$', SBUserList.as_view(), name='user-list'),
    url(r'^search-user/(?P<username>.*)/$', get_user, name='user-list'),
    url(r'^add-trackee/(?P<username>.*)/$', add_trackee, name='add-trackee'),
    url(r'^my-trackees/$', my_trackees, name='my-trackee'),
    url(r'^who-tracks-me/$', who_are_all_tracking_me, name='who-tracks-me'),
    url(r'^password-reset/$', PasswordResetView.as_view(), name='mobile_reset_password'),
    url(r'^departments/$', department_list, name='department-list'),
    url(r'^employee/map/(?P<username>.*)/$', map_employee, name='employee-detail'),
    url(r'^get-employees-by-department/(?P<department_id>.*)/$', get_employees_by_department, name='get-employees-by-department'),
]