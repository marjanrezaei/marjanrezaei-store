from rest_framework.permissions import BasePermission
from accounts.models import UserType
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render


# ---------------- CBV Mixins ----------------
class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if getattr(request.user, 'type', None) != UserType.admin:
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if getattr(request.user, 'type', None) != UserType.customer:
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)


# ---------------- DRF Permissions ----------------
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'type', None) == UserType.admin


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'type', None) == UserType.customer
