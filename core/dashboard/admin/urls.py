from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path("home/", views.AdminDashboardHomeView.as_view(), name="home"),
    
]
