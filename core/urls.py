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
from django.urls import path, include
from .views import AffiliationViewSet, EntityViewSet, UserViewSet, SelfView, TagViewSet, EntityGenericMaterialViewSet, EntitySpecificMaterialViewSet, EntitySpecificMaterialInstanceViewSet

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'affiliations', AffiliationViewSet)
router.register(r'entities', EntityViewSet)
router.register(r'tags', TagViewSet)

router_entities = routers.NestedSimpleRouter(router, r'entities', lookup='entity')
router_entities.register(r'genericmaterials',EntityGenericMaterialViewSet,basename='genericmaterials')
router_entities.register(r'specificmaterials',EntitySpecificMaterialViewSet,basename='specificmaterials')

router_specific_materials = routers.NestedSimpleRouter(router_entities, r'specificmaterials', lookup='specificmaterial')
router_specific_materials.register(r'instances', EntitySpecificMaterialInstanceViewSet, basename='instances')

urlpatterns = [
    path('self/', SelfView.as_view()),
    path('', include(router.urls)),
    path('', include(router_entities.urls)),
    path('', include(router_specific_materials.urls)),

]


