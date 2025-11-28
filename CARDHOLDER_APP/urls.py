from rest_framework.routers import DefaultRouter
from CARDHOLDER_APP.views import CardholderViewSet

router = DefaultRouter()

router.register("cardholder", CardholderViewSet, basename="cardholder")

urlpatterns = router.urls
