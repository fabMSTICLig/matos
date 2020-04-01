from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet, SelfView, AffiliationViewSet, organizationListView, PersonViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/gestion/users', UserViewSet)
router.register(r'api/gestion/persons', PersonViewSet)
router.register(r'api/gestion/affiliations', AffiliationViewSet)
router.register(r'api/gestion/organizations', organizationListView)

urlpatterns = [
    path('', include(router.urls)),
    path('self/', SelfView.as_view())
]
