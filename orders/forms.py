import re

from django import forms

class OrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[('0', False), ('1', True)])
    requires_delivery = forms.ChoiceField(choices=[('0', False), ('1', True)])

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']

        if phone[0] == '+':
            phone = phone[1:]
        
        pattern = r'[78]\d{10}'
        if not re.fullmatch(pattern, phone):
            raise forms.ValidationError('Номер введен не верно')
        
        return phone
        
     