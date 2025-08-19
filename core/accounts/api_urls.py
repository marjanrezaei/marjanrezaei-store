from django.urls import path
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('register/', api_views.RegisterView.as_view(), name='register-api'),
    path('login/', api_views.MyTokenObtainPairView.as_view(), name='login-api'),
]
