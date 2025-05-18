from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners of a ticket or admins to view/edit it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.reservation.user == request.user 