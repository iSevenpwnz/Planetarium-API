from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from rest_framework import status


class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = ["email", "first_name", "last_name", "id"]
    ordering = ["id"]

    def get_queryset(self):
        # Адміністратори бачать усіх користувачів.
        # Для інших дій, таких як retrieve, update, destroy,
        # дозвіл IsSelfOrAdmin буде контролювати доступ на рівні об'єкта.
        # Тому базовий queryset може бути User.objects.all(),
        # а IsSelfOrAdmin відфільтрує, якщо не адмін і не власник.
        return User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
        elif self.action == "me":
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "register":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path="me",
    )
    def me(self, request):
        user = request.user
        if request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            self.get_serializer(user).data, status=status.HTTP_201_CREATED
        )
