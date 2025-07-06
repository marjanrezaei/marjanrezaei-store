from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from accounts.models import UserType

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