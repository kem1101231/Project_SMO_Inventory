from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^create_acct/$', views.create_acct, name = 'create_acct'),
    url(r'^createAcct/$', views.createAcct, name = 'createAcct'),
    url(r'^chckUname/$', views.chckUname, name = 'chckUname'),
    url(r'^chckIdnum/$', views.chckIdnum, name = 'chckIdnum'),
    url(r'^getUserAccessType/$', views.getUserAccessType, name = 'getUserAccessType'),
    url(r'^chckPass/$', views.chckPass, name = 'chckPass'),
    url(r'^getEmpDetails/$', views.getEmpDetails, name = 'getEmpDetails'),
    url(r'^create_admin/$', views.create_admin, name = 'create_admin'),
    ]
 
