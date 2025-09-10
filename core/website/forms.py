from django import forms
from django.utils.translation import gettext_lazy as _

from .models import NewsLetterModel, ContactModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'details']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email Address'),
            'phone_number': _('Phone Number (optional)'),
            'details': _('Message'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('First Name'),
                'id': 'hireUsFormFirstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('Last Name'),
                'id': 'hireUsFormLastName'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('email@site.com'),
                'id': 'hireUsFormWorkEmail'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('e.g. +971501234567'),
                'id': 'hireUsFormPhone'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 4,
                'placeholder': _('Write your message here...'),
                'id': 'hireUsFormDetails'
            }),
        } 
    
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetterModel
        fields = '__all__'
        
         
