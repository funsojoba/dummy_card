from rest_framework.routers import DefaultRouter
from AUTH_APP.views import AuthViewSet

router = DefaultRouter()


router.register("auth", AuthViewSet, basename="auth")


urlpatterns = router.urls
