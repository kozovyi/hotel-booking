from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.user == request.user
        return bool(request.user and request.user.is_staff or is_owner)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)
