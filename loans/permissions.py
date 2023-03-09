from rest_framework import permissions
from rest_framework.views import Request, View


class LoanPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        if request.user.is_authenticated and request.user.is_superuser:
            return True
        
        if request.user.situation == "normal" and request.method not in permissions.SAFE_METHODS:
            return True
        
        return False
