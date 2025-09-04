from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import CustomerRequiredMixin
from django.contrib.auth import views as auth_views
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from accounts.models import Profile
from core.utils.image_utils import handle_profile_image




class CustomerSecurityEditView(CustomerRequiredMixin, LoginRequiredMixin, auth_views.PasswordChangeView, SuccessMessageMixin):
    template_name = 'dashboard/customer/profile/security-edit.html'
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy('dashboard:customer:security-edit')
    success_message = 'بروزرسانی پسورد با موفقیت انجام شد'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class CustomerProfileEditView(CustomerRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'dashboard/customer/profile/profile-edit.html'
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = 'بروزرسانی پروفایل با موفقیت انجام شد'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    
class CustomerProfileImageEditView(CustomerRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = Profile
    fields = ["image"]
    template_name = 'dashboard/customer/profile/profile-edit.html'
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = 'بروزرسانی تصویر پروفایل با موفقیت انجام شد'

    def form_valid(self, form):
        profile = self.get_object()
        new_image = self.request.FILES.get('image')
        host = self.request.get_host()

        handle_profile_image(profile, new_image, host)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
    
    def form_invalid(self, form): 
        messages.error(self.request, "ارسال تصویر با مشکل مواجه شده لطفا مجدد تلاش نمایید")
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
