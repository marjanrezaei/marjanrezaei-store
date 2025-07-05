from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerDashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/home.html'