from django.contrib.auth import update_session_auth_hash, views as auth_views, get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import timedelta
import json
from .tasks import send_reset_email 
from .forms import AuthenticationForm

User = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        request = self.request

        # Save guest cart from session before login (login flushes session)
        guest_cart = request.session.get('cart', {}).copy()

        # Proceed with login (flushes session)
        response = super().form_valid(form)

        # Merge guest cart into new session cart
        session_cart = request.session.get('cart', {})
        for pid, qty in guest_cart.items():
            session_cart[pid] = session_cart.get(pid, 0) + qty

        request.session['cart'] = session_cart
        request.session.modified = True

        # Prevent logout due to session key change
        update_session_auth_hash(request, request.user)

        return response


class LogoutView(auth_views.LogoutView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    template_name = "accounts/password_reset.html"
    success_url = "/accounts/login"

    def form_valid(self, form):
        messages.success(self.request, _("Password reset link has been sent to your email."))
        email = form.cleaned_data.get('email')
        # Schedule sending email asynchronously with 48h ETA
        send_reset_email.apply_async((email,), eta=now() + timedelta(hours=48))
        return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = "/accounts/login"

    def form_valid(self, form):
        messages.success(self.request, _("Your password was changed successfully. Please log in."))
        return super().form_valid(form)


@csrf_exempt
def check_email_exists(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        exists = User.objects.filter(email__iexact=email).exists()
        return JsonResponse({"exists": exists})

    return JsonResponse({"error": "POST method required"}, status=405)
