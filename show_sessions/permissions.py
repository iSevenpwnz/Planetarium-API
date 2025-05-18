from rest_framework import permissions


class ShowSessionPermissions:
    """
    Custom permissions for ShowSession views.
    """
    @classmethod
    def get_permissions(cls, action):
        if action in ["list", "retrieve", "available_seats"]:
            permission_classes = [permissions.AllowAny]
        elif action == "book":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes] 