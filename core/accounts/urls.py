from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views  

app_name = 'accounts'

urlpatterns = [
    path("signup/", TemplateView.as_view(template_name="accounts/signup.html"), name="signup"), 
    path('login/', views.LoginView.as_view(), name='login'),      
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    path('reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('check-email/', views.CheckEmailExistsView.as_view(), name='check-email'),     
]
