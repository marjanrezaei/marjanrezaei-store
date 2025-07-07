from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import AdminRequiredMixin
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from accounts.models import Profile



class AdminSecurityEditView(AdminRequiredMixin, LoginRequiredMixin, auth_views.PasswordChangeView, SuccessMessageMixin):
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('dashboard:admin:security-edit')
    success_message = 'بروزرسانی پسورد با موفقیت انجام شد'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class AdminProfileEditView(AdminRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'dashboard/admin/profile/profile-edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = 'بروزرسانی پروفایل با موفقیت انجام شد'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
class AdminProfileImageEditView(AdminRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    http_method_names = ['post']
    model = Profile
    fields = [
        "image"  
    ]
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = 'بروزرسانی تصویر پروفایل با موفقیت انجام شد'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def form_invalid(self, form): 
        messages.error(self.request, "ارسال تصویر با مشکل مواجه شده لطفا مجدد تلاش نمایید")
        return redirect(self.success_url)
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    
