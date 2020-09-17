from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        