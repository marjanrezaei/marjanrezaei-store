from django.urls import path
from .. import views

urlpatterns = [
    path("home/", views.AdminDashboardHomeView.as_view(), name="home"),
    
    ]