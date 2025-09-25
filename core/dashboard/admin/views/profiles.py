from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from dashboard.permissions import AdminRequiredMixin
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProfileImageForm
from accounts.models import Profile
from core.utils.image_utils import handle_profile_image


class AdminSecurityEditView(AdminRequiredMixin, LoginRequiredMixin, auth_views.PasswordChangeView, SuccessMessageMixin):
    """
    Admin view to change password
    """
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('dashboard:admin:security-edit')
    success_message = _('Password updated successfully')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class AdminProfileEditView(AdminRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    Admin view to edit profile information (excluding image)
    """
    template_name = 'dashboard/admin/profile/profile-edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = _('Profile updated successfully') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class AdminProfileImageEditView(AdminRequiredMixin, LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    Admin view to edit profile image
    """
    model = Profile
    form_class = AdminProfileImageForm
    fields = ["image"]
    template_name = 'dashboard/admin/profile/profile-edit.html'
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = _('Profile image updated successfully') 

    def form_valid(self, form):
        profile = self.get_object()
        new_image = self.request.FILES.get('image')
        host = self.request.get_host()

        handle_profile_image(profile, new_image, host)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, _("Failed to upload image. Please try again.")) 
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
