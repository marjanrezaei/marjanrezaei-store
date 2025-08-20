from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path("completed/", views.OrderCompletedView.as_view(), name="completed"),
    path("failed/", views.OrderFailedView.as_view(), name="failed"),
]
