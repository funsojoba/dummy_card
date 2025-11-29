from rest_framework.routers import DefaultRouter
from CARD_APP.views import CardViewSet


router = DefaultRouter()


router.register("card", CardViewSet, basename="card")

urlpatterns = router.urls
