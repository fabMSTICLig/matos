"""djangovue URL Configuration

self/
users/
affiliations/
tags/
entities/
entities/(entity_pk)/genericmaterials/
entities/(entity_pk)/specificmaterials/
entities/(entity_pk)/specificmaterials/(specificmaterial_pk)/instances
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


