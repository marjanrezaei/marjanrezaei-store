from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import UserTypeRequiredMixin
from accounts.models import UserType

class CustomerDashboardHomeView(UserTypeRequiredMixin, LoginRequiredMixin, TemplateView):
    required_user_type = UserType.customer
    template_name = 'dashboard/customer/home.html'