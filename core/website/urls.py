from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter/', views.NewsletterView.as_view(), name='newsletter'),
    
    path('migrate/', views.MigrateView.as_view(), name='migrate'),
    path("test-email/", views.test_email),
    path("test-db/", views.test_db),
    
]
