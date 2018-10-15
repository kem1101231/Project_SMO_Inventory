from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^pr/$', views.pr, name = 'pr'),
    url(r'^accounts/$', views.accounts, name = 'accounts'),
    url(r'^accounts/par_details/$', views.parDetails, name = 'parDetails'),
    url(r'^notifs/$', views.notifications, name = 'notifications'),
    url(r'^pr/pr_details/$', views.prDetails, name = 'prDetails'),
    url(r'^displayReqDetails/$', views.displayReqDetails, name = 'displayReqDetails'),
    url(r'^displayPARDetails/$', views.displayPARDetails, name = 'displayPARDetails'),
    url(r'^updateAbstract/$', views.updateAbstract, name = 'updateAbstract'),
    #url(r'^output/$', views.return_data),
    ]
 
