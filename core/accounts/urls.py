from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('check-email/', views.check_email_exists, name='check-email'),

    # path('register/', views.RegisterView.as_view(), name='register'),
  
   
]   