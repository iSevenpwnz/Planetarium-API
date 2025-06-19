from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from shows.views import AstronomyShowViewSet, ShowThemeViewSet
from domes.views import PlanetariumDomeViewSet
from show_sessions.views import ShowSessionViewSet
from bookings.views import ReservationViewSet
from tickets.views import TicketViewSet
from users.views import UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Planetarium API",
        default_version="v1",
        description="API для онлайн-бронювання квитків у планетарії",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"astronomy-shows", AstronomyShowViewSet)
router.register(r"show-themes", ShowThemeViewSet)
router.register(r"planetarium-domes", PlanetariumDomeViewSet)
router.register(r"show-sessions", ShowSessionViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"tickets", TicketViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/", include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
