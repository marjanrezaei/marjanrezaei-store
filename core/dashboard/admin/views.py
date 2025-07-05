from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AdminDashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/home.html'