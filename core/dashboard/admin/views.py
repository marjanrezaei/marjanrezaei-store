from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import UserTypeRequiredMixin
from accounts.models import UserType


class AdminDashboardHomeView(UserTypeRequiredMixin, LoginRequiredMixin, TemplateView):
    required_user_type = UserType.admin
    template_name = 'dashboard/admin/home.html'