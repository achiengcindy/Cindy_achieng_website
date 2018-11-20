from django import forms
from .models import Order

class checkoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','postal_code', 'city']
