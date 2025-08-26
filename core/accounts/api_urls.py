from django.urls import path
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path("activation/<str:token>/", api_views.ActivationApiView.as_view(), name="activation"),
    path("register/", api_views.RegisterAPIView.as_view(), name="register-api"),
    path('login/', api_views.MyTokenObtainPairAPIView.as_view(), name='login-api'),
    path('reset-password/', api_views.PasswordResetAPI.as_view(), name='reset-password-api'),  
    path("password-confirm/", api_views.PasswordResetConfirmJWTAPI.as_view(), name="password-reset-confirm-api"),
]
