from django import forms
from accounts.validators import validate_iranian_phone

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(
        max_length=11,
        validators=[validate_iranian_phone])
    email = forms.EmailField(required=True)
    details = forms.CharField(widget=forms.Textarea, required=True)
    
