from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
import json
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import get_user_model
from .tasks import send_reset_email

User = get_user_model()


class LoginView(AuthLoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True 


class PasswordResetView(auth_views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    template_name = "accounts/password_reset.html"
    success_url = "/accounts/login"

    def form_valid(self, form):
        messages.success(self.request, _("Password reset link has been sent to your email."))
        email = form.cleaned_data.get("email")
        # Send async email after 48h
        send_reset_email.apply_async((email,), eta=now() + timedelta(hours=48))
        return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = "/accounts/login"

    def form_valid(self, form):
        messages.success(self.request, _("Your password was changed successfully. Please log in."))
        return super().form_valid(form)
 
    
class CheckEmailExistsView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        exists = User.objects.filter(email__iexact=email).exists()
        return JsonResponse({"exists": exists})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method required"}, status=405)