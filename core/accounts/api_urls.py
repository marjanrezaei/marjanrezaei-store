from django.urls import path
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('register/', api_views.RegisterAPIView.as_view(), name='register-api'),
    path('login/', api_views.MyTokenObtainPairAPIView.as_view(), name='login-api'),
    path('reset-password/', api_views.PasswordResetAPI.as_view(), name='reset-password-api'),
    path('password-confirm/<uidb64>/<token>/', api_views.PasswordResetConfirmAPI.as_view(), name='reset-password-confirm-api'),
    path('check-email/', api_views.CheckEmailExistsAPI.as_view(), name='check-email-api'),     
]
