from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm 
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .tasks import send_reset_email  # Celery Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta
from django.utils.timezone import now


User = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    

class LogoutView(auth_views.LogoutView):
    pass
    

class PasswordResetView(auth_views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    template_name = "accounts/password_reset.html"
    success_url = "/accounts/login"

    def form_valid(self, form):
        messages.success(self.request, "لینک تغییر رمز عبور به ایمیل شما ارسال شد")
        email = form.cleaned_data.get('email')
        send_reset_email.apply_async((email,), eta=now() + timedelta(hours=48))

        return super().form_valid(form)
    

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = "/accounts/login"
    def form_valid(self, form):
        messages.success(self.request, "رمز عبور شما با موفقیت تغییر کرد. لطفاً وارد شوید.")
        return super().form_valid(form)


@csrf_exempt 
def check_email_exists(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email", "")
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({"exists": exists})
    