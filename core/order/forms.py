from django import forms
from order.models import UserAddressModel

class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckOutForm, self).__init__(*args, **kwargs)
        
    def clean_address_id(self):
        address_id = self.cleaned_data['address_id']
        
        user = self.request.user
        try:
            address = UserAddressModel.objects.get(id=address_id, user=user)
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("Invalid address for the requested user.")
        
        return address