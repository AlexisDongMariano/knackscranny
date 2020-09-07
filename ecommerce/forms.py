from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': '1234 Main Street'}))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': 'Apartment or suite'}))
    country = CountryField(blank_label='(select country)')
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
                }))
    chk_same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class':'custom-control-input'
        }
    ))
    chk_save_info = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class':'custom-control-input'
        }
    ))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={
            'class':'custom-control-input'
        }
    ), choices=PAYMENT_CHOICES)