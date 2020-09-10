from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    shipping_address1 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': '1234 Main Street'}))
    shipping_address2 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': 'Apartment or suite'}))
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(
        attrs={'class': 'custom-select d-block w-100'}, layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'))
    shipping_zip_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    billing_address1 = forms.CharField(required=False, widget=forms.TextInput(
    attrs={'class': 'form-control',
            'placeholder': '1234 Main Street'}))
    billing_address2 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': 'Apartment or suite'}))
    billing_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(
        attrs={'class': 'custom-select d-block w-100'}, layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'))
    billing_zip_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
        
    chk_same_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input'}))
    chk_save_shipping_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input'}))
    chk_save_billing_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class':'custom-control-input'}), choices=PAYMENT_CHOICES)