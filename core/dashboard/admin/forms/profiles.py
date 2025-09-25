from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please correct it."
        ),
        "password_mismatch": _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control text-center',
            'placeholder': _('Enter your old password')
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control text-center',
            'placeholder': _('Enter your new password')
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control text-center',
            'placeholder': _('Repeat your new password')
        })


class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('First Name')
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Last Name')
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control text-center',
            'placeholder': _('Phone Number')
        })


class AdminProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'image_url']
        widgets = {
            'image_url': forms.TextInput(attrs={'placeholder': _('Image URL')}),
        }
