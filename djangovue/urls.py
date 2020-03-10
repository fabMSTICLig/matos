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
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url, include
from api.views import sample_api, signup_success, productListViewSet, productInstanceListView, index, organizationListView, get_users, UserInstanceView, productDetailViewSet
import django_cas_ng.views
from rest_framework import routers
from adminplatform.urls import router as adminrouter

router = routers.DefaultRouter()
router.register(r'api/equipments', productListViewSet)
router.register(r'api/products-instance', productInstanceListView)
router.registry.extend(adminrouter.registry)

urlpatterns = [
    url(r'^$', view=TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/login',  django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('api/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    url(r'^home/', index),
    url(r'^api/users/', get_users.as_view()),
    url(r'^api/organizations/(?P<pk>[0-9]+)$', views.organizationDetail.as_view()),
    url(r'^api/equipment/(?P<pk>[0-9]+)$', views.productDetailViewSet.as_view()),
    url(r'^api/families/$', views.family_list.as_view()),
    url(r'^api/families/(?P<pk>[0-9]+)$', views.family_detail.as_view()),
    url(r'^locations/$', views.location_list.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)$', views.location_detail.as_view()),
    url(r'^transactions/$', views.transaction_list.as_view()),
    url(r'^transactions/(?P<pk>[0-9]+)$', views.transaction_detail.as_view()),
    path('api/sampleapi', sample_api),
    path('api/self/', UserInstanceView.as_view()),
    url(r'^signup-success/$', signup_success),
    url(r'^person-create/$', views.PersonView.as_view()),
    path('', include(router.urls)),

]


