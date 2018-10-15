from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.index, name = 'index'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^pr/(?P<refData>\w+)/details$', views.pr_Details, name = 'pr_Deatils'),
	url(r'^account/$', views.accounts, name = 'accounts'),
	url(r'^all_request/$', views.allPR, name = 'allPR'),
	url(r'^pending_request/$', views.pendingPR, name = 'pendingPR'),
	url(r'^pending_request/pr_details/$', views.pendingPRDetails, name = 'pendingPRDetails'),
	url(r'^notifs/(?P<refData>\w+)/$', views.notifications, name = 'notifications'),
	url(r'^displayPRdetails/$', views.displayPendingPRDetails, name = 'displayPendingPRDetails'),
	url(r'^decidePR/$', views.decidePR, name = 'decidePR'),
	url(r'^account/departments/$', views.departments, name = 'departments'),
	url(r'^acctDetails/$', views.acctdetails, name = 'acctdetails'),
	url(r'^account/item_list$', views.itemList, name = 'itemList'),
	url(r'^pending_request/departments$', views.departmentPendingPR, name = 'departmentPendingPR'),
	url(r'^pendingListDetails/$', views.pendingListDetails, name = 'pendingListDetails'),
	url(r'^all_request/departments/$', views.departmentPR, name = 'departmentPR'),
	url(r'^prListDetails/$', views.prListDetails, name = 'prListDetails'),
	url(r'^pending_request/list$', views.pendingPRList, name = 'pendingPRList'),
	url(r'^all_request/list$', views.prList, name = 'prList'),
	url(r'^declinePR/$', views.declinePR, name = 'declinePR'),
	url(r'^getPendingInitPR/$', views.getPendingInitPR, name = 'getPendingInitPR'),
	url(r'^getPendingPR/$', views.getPendingPR, name = 'getPendingPR'),
	url(r'^displayPendingPRDetails/$', views.displayPendingPRDetails, name = 'displayPendingPRDetails'),
	url(r'^displayPendingPRDetailsFromIndex/$', views.displayPendingPRDetailsFromIndex, name = 'displayPendingPRDetailsFromIndex'),
	url(r'^setPRCookie/$', views.setPRCookie, name = 'setPRCookie'),
	url(r'^getNotifNum/$', views.getNotifNum, name = 'getNotifNum'),
	url(r'^getTaskNum/$', views.getTaskNum, name = 'getTaskNum'),
	url(r'^getNotifs/$', views.getNotifs, name = 'getNotifs'),
	url(r'^getTasks/$', views.getTasks, name = 'getTasks'),	
	


    ]
 
