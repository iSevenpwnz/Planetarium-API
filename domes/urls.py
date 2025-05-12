from rest_framework.routers import DefaultRouter
from domes.views import PlanetariumDomeViewSet

router = DefaultRouter()
router.register(r"planetarium-domes", PlanetariumDomeViewSet)

urlpatterns = router.urls
