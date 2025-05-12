from rest_framework.routers import DefaultRouter
from bookings.views import ReservationViewSet

router = DefaultRouter()
router.register(r"reservations", ReservationViewSet)

urlpatterns = router.urls
