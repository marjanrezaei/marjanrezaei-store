from django.urls import path
from .. import views

urlpatterns = [
    path("home/", views.CustomerDashboardHomeView.as_view(), name="home"),
    
    ]