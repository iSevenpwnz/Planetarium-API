from rest_framework.routers import DefaultRouter
from show_sessions.views import ShowSessionViewSet

router = DefaultRouter()
router.register(r"show-sessions", ShowSessionViewSet)

urlpatterns = router.urls
