from django.urls import path, include
from .views import UserViewSet, SelfView, AffiliationViewSet, organizationListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/gestion/users', UserViewSet)
router.register(r'api/gestion/organizations', organizationListView)
router.register(r'api/gestion/affiliations', AffiliationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('self/', SelfView.as_view())
]
