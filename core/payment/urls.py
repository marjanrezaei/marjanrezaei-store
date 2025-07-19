from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('verify', views.PaymentVerifyView.as_view(), name='verify'),

]