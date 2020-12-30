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
from .views import AffiliationViewSet, EntityViewSet, UserViewSet, SelfView, TagViewSet, EntityGenericMaterialViewSet, EntitySpecificMaterialViewSet, EntitySpecificMaterialInstanceViewSet, GenericMaterialViewSet, SpecificMaterialViewSet, SpecificMaterialInstanceViewSet, LoanViewSet, RGPDAcceptView, PersonalDataView

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'affiliations', AffiliationViewSet)
router.register(r'entities', EntityViewSet)
router.register(r'genericmaterials', GenericMaterialViewSet, basename="public-genericmaterials")
router.register(r'specificmaterials', SpecificMaterialViewSet, basename="public-specificmaterials")
router.register(r'tags', TagViewSet)
router.register(r'loans', LoanViewSet)

router_publicspecificmaterials = routers.NestedSimpleRouter(router, r'specificmaterials', lookup='specificmaterial')
router_publicspecificmaterials.register(r'instances', SpecificMaterialInstanceViewSet, basename='public-instances')

router_entities = routers.NestedSimpleRouter(router, r'entities', lookup='entity')
router_entities.register(r'genericmaterials',EntityGenericMaterialViewSet,basename='genericmaterials')
router_entities.register(r'specificmaterials',EntitySpecificMaterialViewSet,basename='specificmaterials')

router_specific_materials = routers.NestedSimpleRouter(router_entities, r'specificmaterials', lookup='specificmaterial')
router_specific_materials.register(r'instances', EntitySpecificMaterialInstanceViewSet, basename='instances')

#router_loans_specific = routers.NestedSimpleRouter(router_specific_materials, r'instances', lookup='instance')
#router_loans_specific.register(r'loans',SpecificMaterialLoanViewSet,basename='loans')

#router_loans_generic = routers.NestedSimpleRouter(router_entities, r'genericmaterials', lookup='genericmaterial')
#router_loans_generic.register(r'loans',GenericMaterialLoanViewSet,basename='loans')

urlpatterns = [
    path('self/', SelfView.as_view()),
    path('self/data/', PersonalDataView.as_view()),
    path('self/rgpd/', RGPDAcceptView.as_view()),
    path('', include(router.urls)),
    path('', include(router_entities.urls)),
    path('', include(router_specific_materials.urls)),
    path('', include(router_publicspecificmaterials.urls)),
 #   path('', include(router_loans_specific.urls)),
 #   path('', include(router_loans_generic.urls))

]
