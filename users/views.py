from .forms import UserRegisterForm, CustomerUpdateForm
from .models import Customer
from ecommerce.views import get_session
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
       return redirect('ecommerce:home')
    else:
        if request.method == 'POST':
            print(request.POST)
            print('================================', request.body)
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                # create customer object and assign fields
                customer = get_session(request)
                user = User.objects.filter(username=form.cleaned_data.get('username')).first()
                customer.user = user
                customer.first_name = form.cleaned_data.get('first_name')
                customer.last_name = form.cleaned_data.get('last_name')
                customer.email = form.cleaned_data.get('email')
                customer.contact1 = form.cleaned_data.get('contact1')
                customer.contact2 = form.cleaned_data.get('contact2')
                customer.save()

                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created, you can now login!')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


def profile(request):
    customer = Customer.objects.filter(user=request.user).first()
    form = CustomerUpdateForm(instance=customer)
    context = {
        'form': form,
        'customer': customer,
        'first_name': customer.first_name.capitalize(),
        'last_name': customer.last_name.capitalize(),
    }
    return render(request, 'users/profile.html', context)