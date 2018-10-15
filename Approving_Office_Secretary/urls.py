from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^pr/$', views.allPR, name = 'allPR'),
    url(r'^pr/(?P<refData>\w+)/details/$', views.prDetails, name = 'prDetails'),
    url(r'^pending_request/pr_details/$', views.pendingPRDetails, name = 'pendingPRDetails'),
    url(r'^pr/departments/$', views.departmentPR, name = 'departmentPR'),
    url(r'^pr/list/$', views.prList, name = 'prList'),
    url(r'^number_a_pr/$', views.numPR, name = 'numPR'),
    url(r'^notifs/$', views.displayNotif, name = 'displayNotif'),
    url(r'^number_a_pr/pr_details/$', views.prForNumDetails, name = 'prForNumDetails'),
    url(r'^numtheReq/$', views.numtheReq, name = 'numtheReq'),
    url(r'^prListDetails/$', views.prListDetails, name = 'prListDetails'),
    url(r'^addReqQuotation/$', views.addReqQuotation, name = 'addReqQuotation'),
    url(r'^getSupplierDetails/$', views.getSupplierDetails, name = 'getSupplierDetails'),
    url(r'^findComp/$', views.findComp, name = 'findComp'),
    url(r'^findRepComp/$', views.findRepComp, name = 'findRepComp'),
    url(r'^getPRItems/$', views.getPRItems, name = 'getPRItems'),
    url(r'^getEmployeeData/$', views.getEmployeeData, name = 'getEmployeeData'),
    url(r'^notifs/(?P<refData>\w+)/$', views.notifications, name = 'notifications'),
    url(r'^update_location/$', views.updateLocation, name = 'updateLocation'),
    url(r'^decidePR/$', views.decidePR, name = 'decidePR'),
    url(r'^declinePR/$', views.declinePR, name = 'declinePR'),

    ]
 
