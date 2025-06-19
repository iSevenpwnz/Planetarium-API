from rest_framework import permissions


class ShowThemePermissions:
    """
    Custom permissions for ShowTheme views.
    """
    @classmethod
    def get_permissions(cls, action):
        if action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class AstronomyShowPermissions:
    """
    Custom permissions for AstronomyShow views.
    """
    @classmethod
    def get_permissions(cls, action):
        if action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif action == "upload_image":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes] 