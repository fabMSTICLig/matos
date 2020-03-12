from django.urls import path, include
from .views import UserViewSet, SelfView, AffiliationViewSet, organizationListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gestion/users', UserViewSet)
router.register(r'gestion/organizations', organizationListView)
router.register(r'gestion/affiliations', AffiliationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('self/', SelfView.as_view())
]
