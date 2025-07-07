from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import AdminRequiredMixin


class AdminDashboardHomeView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/home.html'
