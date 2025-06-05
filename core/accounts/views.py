from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm

class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    