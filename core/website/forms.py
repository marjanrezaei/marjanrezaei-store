from django import forms
from .models import NewsLetterModel, ContactModel


class ContactForm(forms.ModelForm):
     class Meta:
        model = ContactModel
        fields = '__all__' 
    
    
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetterModel
        fields = '__all__'
        
         
