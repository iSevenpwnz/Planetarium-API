from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to edit only their own profiles or admins to edit any profile.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class UserPermissions:
    """
    Custom permissions for User views.
    """
    @classmethod
    def get_permissions(cls, action):
        """
        Returns permissions based on action.
        """
        if action == "create":
            permission_classes = [permissions.IsAdminUser]
        elif action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif action == "retrieve":
            permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
        elif action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
        elif action == "me":
            permission_classes = [permissions.IsAuthenticated]
        elif action == "register":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes] 