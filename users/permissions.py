from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAdminOrUserOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user.is_superuser or request.user == obj


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        if request.method == "GET" and request.user.is_authenticated:
            return True
