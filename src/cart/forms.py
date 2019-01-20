from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
    
    # check if cookie isenabled andrequest usertodo so if not
    # def clean(self):
    #     if self.request:
    #         if not self.request.session.test_cookie_worked():
    #             raise forms.ValidationError("Cookies must be enabled.")
    #     return self.cleaned_data





