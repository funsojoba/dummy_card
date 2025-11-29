from rest_framework.routers import DefaultRouter
from WEBHOOK_APP.views import WebhookViewSet

router = DefaultRouter()


router.register("webhook", WebhookViewSet, basename="webhook")

urlpatterns = router.urls
