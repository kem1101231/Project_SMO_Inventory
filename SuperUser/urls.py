from django.shortcuts import render

# Create your views here.
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^users/$', views.users, name = 'users'),
    url(r'^offices/$', views.offices, name = 'offices'),
    url(r'^offices/(?P<refData>\w+)/details/$', views.officeDetails, name = 'officeDetails'),
    url(r'^key_users/$', views.keyUsers, name = 'keyUsers'),
    url(r'^add_employee/$', views.addEmployee, name = 'addEmployee'),
    url(r'^employees/$', views.employees, name = 'employees'),
    url(r'^employees/(?P<refData>\w+)/details/$', views.empDetails, name = 'empDetails'),
    url(r'^updateOfficeHead/$', views.updateOfficeHead, name = 'updateOfficeHead'),
    url(r'^updateUserStatus/$', views.updateUserStatus, name = 'updateUserStatus'),
    url(r'^logs/$', views.logs, name = 'logs'),
    url(r'^addoffice/$', views.addOffice, name = 'addOffice'),
    url(r'^uploadTest/$', views.uploadTest2, name = 'uploadTest2'),
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    url(r'^updateUserType/$', views.updateUserType, name='updateUserType'),
    url(r'^getAllOffices/$', views.getAllOffices, name='getAllOffices'),
    url(r'^tranferuser/$', views.tranferuser, name='tranferuser'),
   
    #url(r'^output/$', views.return_data),
    ]
 
