from rest_framework.routers import DefaultRouter
from shows.views import AstronomyShowViewSet, ShowThemeViewSet

router = DefaultRouter()
router.register(r"astronomy-shows", AstronomyShowViewSet)
router.register(r"show-themes", ShowThemeViewSet)

urlpatterns = router.urls
