from rest_framework import permissions


class PlanetariumDomePermissions:
    """
    Custom permissions for PlanetariumDome views.
    """
    @classmethod
    def get_permissions(cls, action):
        """
        Returns the list of permissions that this view requires.
        """
        if action in ["list", "retrieve", "capacity", "sessions"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes] 