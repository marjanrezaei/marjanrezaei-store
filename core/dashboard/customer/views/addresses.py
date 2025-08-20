from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import CustomerRequiredMixin

class CustomerAddressManageView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "dashboard/customer/addresses/address-list.html"