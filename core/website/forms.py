from django import forms
from .models import NewsLetter, Contact

class ContactForm(forms.ModelForm):
     class Meta:
        model = Contact
        fields = '__all__'
   
    
    
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'
        
         
