from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from rest_framework import status
from users.permissions import IsSelfOrAdmin, UserPermissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = ["email", "first_name", "last_name", "id"]
    ordering = ["id"]

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        return UserPermissions.get_permissions(self.action)

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
