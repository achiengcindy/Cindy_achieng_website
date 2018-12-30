from django import forms
from .models import Order
from accounts.models import Profile



# class checkoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ( 'phone', 'physical_address','postal_code','city','Estate')


class BillingEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'phone', 'physical_address','postal_code','city','Estate')


""" class checkoutForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = exclude('User','date_of_birth','photo',)

        
class BillingEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ( 'phone', 'physical_address','postal_code','city','Estate')

        def clean_phone(self):
            phone = self.cleaned_data['phone']
            stripped_phone = strip_non_numbers(phone)
            if len(stripped_phone) < 10:
                raise forms.ValidationError('Enter a valid phone number.(e.g.07********)')
            return self.cleaned_data['phone']

       """
