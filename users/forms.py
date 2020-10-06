from .models import Customer, Address
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    contact1 = forms.CharField(max_length=100, required=True, label='Contact number')
    contact2 = forms.CharField(max_length=100, required=False, label='Alternate number')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact1', 'contact2', 'password1', 'password2']

    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'contact1', 'contact2', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'contact1': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'contact2': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control-file clearablefileinput', 'accept': 'image/*'})
            'image': forms.FileInput(attrs={'class': 'custom-file-input', 'accept': 'image/*'})
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class ShippingAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address1', 'address2', 'country', 'zip_code']
        widgets = {
             'address1': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
             'address2': forms.TextInput(attrs={'class': 'form-control'}),
             'country': CountrySelectWidget(
                 attrs={'class': 'custom-select d-block w-100'},
                 layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'
             ),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class BillingAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address1', 'address2', 'country', 'zip_code']
        widgets = {
             'address1': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
             'address2': forms.TextInput(attrs={'class': 'form-control'}),
             'country': CountrySelectWidget(
                 attrs={'class': 'custom-select d-block w-100'},
                 layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'
             ),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }