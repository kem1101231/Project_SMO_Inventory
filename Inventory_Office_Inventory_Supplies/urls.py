from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^add_accounts/$', views.addAcct, name = 'addAcct'),
    url(r'^accounts/$', views.acct, name = 'acct'),
    url(r'^accounts/offices/$', views.offList, name = 'offList'),
    url(r'^accounts/offices/details/$', views.offDetails, name = 'offDetails'),
    url(r'^accounts/personnel/details/$', views.empDetails, name = 'empDetails'),
    url(r'^add_equipement/$', views.addEqui, name = 'addEqui'),
    url(r'^add_receive/$', views.addReceive, name = 'addReceive'),
    url(r'^add_receive_new/$', views.addReceiveNew, name = 'addReceiveNew'),
    url(r'^add_receive_newer/$', views.addReceiveNewer, name = 'addReceiveNewer'),
    url(r'^equipement/$', views.equi, name = 'equi'),
    url(r'^physical_count/$', views.pcp, name = 'pcp'),
    url(r'^receive/$', views.receive, name = 'receive'),
    url(r'^receive/details/$', views.iarDisplayDetails, name = 'iarDisplayDetails'),
    url(r'^waste_material/$', views.waste, name = 'waste'),
    url(r'^add_inventory/$', views.addInven, name = 'addInven'),
    url(r'^inventory/$', views.inven, name = 'inven'),
    url(r'^getPOItems/$', views.getPOItems, name = 'getPOItems'),
    url(r'^getPODetails/$', views.getPODetails, name = 'getPODetails'),
    url(r'^receiveItems/$', views.receiveItems, name = 'receiveItems'),
    url(r'^getAvailableItems/$', views.getAvailableItems, name = 'getAvailableItems'),
    url(r'^addToAcct/$', views.addToAcct, name = 'addToAcct'),
    url(r'^account/departments/$', views.departments, name = 'departments'),
    url(r'^acctDetails/$', views.acctdetails, name = 'acctdetails'),
    url(r'^equipment/details/$', views.equiDetails, name = 'equiDetails'),
    url(r'^equipment/list/$', views.equiList, name = 'equiList'),
    url(r'^items/$', views.itemList, name = 'itemList'),
    url(r'^items/details$', views.itemDetails, name = 'itemDetails'),
    url(r'^search/$', views.search, name = 'search'),
    url(r'^addNewItem/$', views.addNewItem, name = 'addNewItem'),
    url(r'^receive/(?P<refData>\w+)/details/$', views.iarDisplayDetailsFromRef, name = 'iarDisplayDetailsFromRef'),

    ]
 
