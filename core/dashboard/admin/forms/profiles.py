from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_incorrect": _(
            "پسورد قبلی شما اشتباه وارد شده است. لطفا تصحیح نمایید."
        ),
        "password_mismatch": _(" دو پسورد ورودی با یکدیگر مطابقت ندارد "),
    }
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control text-center'
        self.fields['old_password'].widget.attrs['placeholder'] = 'پسورد قبلی را وارد نمایید'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control text-center'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'پسورد جایگزین خود را وارد نمایید'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control text-center'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'پسورد جایگزین خود را مجدد وارد نمایید'


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
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control text-center'

class AdminProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'image_url']