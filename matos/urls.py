"""matos URL Configuration

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
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.views.generic import TemplateView
import django_cas_ng.views

urlpatterns = [
    re_path(r'^$', view=TemplateView.as_view(template_name='index.html')),
    re_path(r'^su/', include('django_su.urls')),
    path('admin/login/', lambda r: redirect("/")),
    path('admin/logout/', lambda r: redirect("/")),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('cas/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('cas/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('api/', include('core.urls')),
]

