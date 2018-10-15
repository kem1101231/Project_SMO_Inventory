from django.conf.urls import url
from . import views

import re

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
    url(r'^pr/$', views.prList, name = 'prList'),
    url(r'^po/$', views.poList, name = 'poList'),
    url(r'^quotations/$', views.quoList, name = 'quoList'),
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
    url(r'^generateIARDocument/$', views.generateIARDocument, name = 'generateIARDocument'),
    url(r'^generatePARDocument/$', views.generatePARDocument, name = 'generatePARDocument'),
    url(r'^generateWMRDocument/(?P<refData>\w+)/$', views.generateWMRDocument, name = 'generateWMRDocument'),
    url(r'^generateOBRDocument/(?P<refData>\w+)/$', views.generateOBRDocument, name = 'generateOBRDocument'),
    url(r'^displayItemOfParticular/$', views.displayItemOfParticular, name = 'displayItemOfParticular'),
    url(r'^displayEquipDetails/$', views.displayEquipDetails, name = 'displayEquipDetails'),
    url(r'^ris/details/$', views.risDetails, name = 'risDetails'),
    url(r'^getRIS/$', views.getRIS, name = 'getRIS'),
    url(r'^displayRISDetails/$', views.displayRISDetails, name = 'displayRISDetails'),
    url(r'^approveRIS/$', views.approveRIS, name = 'approveRIS'),
    url(r'^releaseRIS/$', views.releaseRIS, name = 'releaseRIS'),
    url(r'^getEquiParticulars/$', views.getEquiParticulars, name = 'getEquiParticulars'),
    url(r'^getItemDetails/$', views.getItemDetails, name = 'getItemDetails'),
    url(r'^offices/$', views.offices, name = 'offices'),
    url(r'^ris/$', views.risList, name = 'risList'),
    url(r'^wmr/$', views.wMR, name = 'wMR'),
    url(r'^updateItem/$', views.updateItem, name = 'updateItem'),
    url(r'^search/(?P<refType>\w+)/(?P<refData>\w+)/$', views.searchRedirectDetails, name='searchRedirectDetails'),
    url(r'^po/(?P<refData>\w+)/details/$', views.displayPODetails, name='displayPODetails'),
    url(r'^pr/(?P<refData>\w+)/details/$', views.prDetails, name='prDetails'),
    url(r'^ris/(?P<refData>\w+)/details/$', views.risWithRefDetails, name='risWithRefDetails'),
    url(r'^quotation/(?P<refData>\w+)/details/$', views.rqDetails, name='rqDetails'),
    url(r'^wmr/(?P<refData>\w+)/details/$', views.wmrDetails, name='wmrDetails'),
    url(r'^supply/(?P<refData>\w+)/details/$', views.supplyDetails, name='supplyDetails'),
    url(r'^wmr/create_new/$', views.createWMR, name='createWMR'),
    url(r'^getPARItems/$', views.getPARItems, name = 'getPARItems'),
    url(r'^addNewWMI/$', views.addNewWMI, name = 'addNewWMI'),
    url(r'^receive/(?P<refData>\w+)/details/$', views.iarDisplayDetailsFromRef, name = 'iarDisplayDetailsFromRef'),

    
    ]

    
