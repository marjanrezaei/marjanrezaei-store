from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class UserTypeRequiredMixin(AccessMixin):
    required_user_type = None  # override in your view, e.g. 'admin' or 'customer'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login or default no-permission handler
            return self.handle_no_permission()
        if self.required_user_type and request.user.type != self.required_user_type:
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return super().dispatch(request, *args, **kwargs)
