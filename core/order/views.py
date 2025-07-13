from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import CustomerRequiredMixin

class OrderCheckOutView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "order/checkout.html"