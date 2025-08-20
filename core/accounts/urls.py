from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),      
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    path('reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('check-email/', views.CheckEmailExistsView.as_view(), name='check-email'),     
]
