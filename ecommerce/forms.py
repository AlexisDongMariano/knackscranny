from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


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
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(
        attrs={'class': 'custom-select d-block w-100'}, layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'))
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    chk_same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input'}))
    chk_save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class':'custom-control-input'}), choices=PAYMENT_CHOICES)