from .forms import UserRegisterForm, CustomerUpdateForm, UserUpdateForm
from .models import Customer
from ecommerce.views import get_session
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
def profile(request):
    customer = Customer.objects.filter(user=request.user).first()
    if request.method == 'GET':  
        form = CustomerUpdateForm(instance=customer)
        u_form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
            'u_form': u_form,
            'customer': customer,
            'first_name': customer.first_name.capitalize(),
            'last_name': customer.last_name.capitalize(),
        }
        return render(request, 'users/profile.html', context)

    elif request.method == 'POST':
        form = CustomerUpdateForm(request.POST, request.FILES, instance=customer)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid() and form.is_valid():
            # update the User model instance from the customer form
            new_u_form = u_form.save(commit=False)
            new_u_form.email = form.cleaned_data.get('email')
            new_u_form.first_name = form.cleaned_data.get('first_name')
            new_u_form.last_name = form.cleaned_data.get('last_name')
            new_u_form.save()

            form.save()

            messages.success(request, f'Account has been updated!')    

            return redirect('users:profile')

@login_required
def addresses(request):
    customer = Customer.objects.filter(user=request.user).first()
    if request.method == 'GET':
        return render(request, 'users/addresses.html')