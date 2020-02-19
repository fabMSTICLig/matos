"""djangovue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from api import views
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url, include
from api.views import sample_api, signup_success, productListViewSet
import django_cas_ng.views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/equipments', productListViewSet)

urlpatterns = [
    url(r'^$', view=TemplateView.as_view(template_name='listview/home.html')),
    path('admin/', admin.site.urls),
    path('api/login',  django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('api/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    url(r'^equipments/(?P<pk>[0-9]+)$', views.product_detail.as_view()),
    url(r'^families/$', views.family_list.as_view()),
    url(r'^families/(?P<pk>[0-9]+)$', views.family_detail.as_view()),
    url(r'^locations/$', views.location_list.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)$', views.location_detail.as_view()),
    url(r'^transactions/$', views.transaction_list.as_view()),
    url(r'^transactions/(?P<pk>[0-9]+)$', views.transaction_detail.as_view()),
    path('api/sampleapi', sample_api),
    url(r'^signup-success/$', signup_success),
    url(r'^person-create/$', views.PersonView.as_view()),
    url(r'^organization-create/$', views.OrganizationView.as_view()),
    path('organizations', views.organization_list.as_view()),
    path('', include(router.urls)),



]
