from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import CustomerRequiredMixin


class CustomerDashboardHomeView(CustomerRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/home.html'