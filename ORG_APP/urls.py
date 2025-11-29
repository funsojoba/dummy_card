from rest_framework.routers import DefaultRouter
from ORG_APP.views import OrganizationViewSet


router = DefaultRouter()


router.register("organization", OrganizationViewSet, basename="organization")

urlpatterns = router.urls
