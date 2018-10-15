"""Project_SMO_Inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings

from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^system_admin/', include('SuperUser.urls')),
    url(r'^', include('Login.urls')),
    url(r'^requisitioner/', include('Requisitioner.urls')),
    url(r'^inventory_office/', include('Inventory_Office.urls')),
    url(r'^inventory_office_admin/', include('Inventory_Office_Admin.urls')),
    url(r'^inventory_office_acct_mgr/', include('Inventory_Office_Acct_Mgr.urls')),
    url(r'^inventory_office_inv_clerk/', include('Inventory_Office_Inventory_Clerk.urls')),
    url(r'^inventory_office_rec_off/', include('Inventory_Office_Receiving_Off.urls')),
    url(r'^inventory_office_sup_off/', include('Inventory_Office_Supply_Officer.urls')),
    url(r'^procurement_office/', include('Procurement_Office.urls')),
    url(r'^approving_officer/', include('Approving_Office.urls')),
    url(r'^approving_officer_representative/', include('Approving_Office_Secretary.urls')),
    url(r'^non_requisitioner/', include('NonRequisitioner.urls')),
    url(r'^accounting/', include('Accounting.urls')),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
