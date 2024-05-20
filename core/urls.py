"""
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault
"""
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
from .views import AffiliationViewSet, EntityViewSet, UserViewSet, SelfView, TagViewSet, EntityGenericMaterialViewSet, EntitySpecificMaterialViewSet, EntitySpecificMaterialInstanceViewSet, LoanViewSet, RGPDAcceptView, PersonalDataView, MaterialsView, RetrieveGenericMaterialsView, RetrieveSpecificMaterialsView, LoanStatsView
from .view_stat import StatsViewSet

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'affiliations', AffiliationViewSet)
router.register(r'entities', EntityViewSet)
router.register(r'tags', TagViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'stats', StatsViewSet,basename='statitiques')

router_entities = routers.NestedSimpleRouter(router, r'entities', lookup='entity')
router_entities.register(r'genericmaterials',EntityGenericMaterialViewSet,basename='genericmaterials')
router_entities.register(r'specificmaterials',EntitySpecificMaterialViewSet,basename='specificmaterials')

router_specific_materials = routers.NestedSimpleRouter(router_entities, r'specificmaterials', lookup='specificmaterial')
router_specific_materials.register(r'instances', EntitySpecificMaterialInstanceViewSet, basename='instances')


urlpatterns = [
    path('self/', SelfView.as_view()),
    path('self/data/', PersonalDataView.as_view()),
    path('self/rgpd/', RGPDAcceptView.as_view()),
    path('loans/stats/', LoanStatsView.as_view()),
    path('materials/', MaterialsView.as_view()),
    path('materials/g/<int:pk>/', RetrieveGenericMaterialsView.as_view(), name='materials-generic-detail'),
    path('materials/s/<int:pk>/', RetrieveSpecificMaterialsView.as_view(), name='materials-specific-detail'),
    path('', include(router.urls)),
    path('entities/<int:entity_pk>/materials/', MaterialsView.as_view(), name="entities-materials"),
    path('', include(router_entities.urls)),
    path('', include(router_specific_materials.urls)),
]
