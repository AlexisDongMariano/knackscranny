from .forms import UserRegisterForm, CustomerUpdateForm, UserUpdateForm, ShippingAddressUpdateForm, BillingAddressUpdateForm
from .models import Customer, Address
from ecommerce.models import Order
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
                form.save() # saving the User model first
                # create Customer object and assign fields
                user = User.objects.filter(username=form.cleaned_data.get('username')).first()
                customer = get_session(request, user) # get customer via session key or create if new
                customer.user = user
                customer.first_name = form.cleaned_data.get('first_name')
                customer.last_name = form.cleaned_data.get('last_name')
                customer.email = form.cleaned_data.get('email')
                customer.contact1 = form.cleaned_data.get('contact1')
                customer.contact2 = form.cleaned_data.get('contact2')
                customer.save()
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

        email_input = form.data.get('email')

        if customer.email != email_input and User.objects.filter(email=email_input).exists():
            messages.error(request, f'Email already exists!')    
            return redirect('users:profile')
        else:
            if u_form.is_valid() and form.is_valid():
                # update the User model instance from the customer form
                new_u_form = u_form.save(commit=False)
                new_u_form.email = email_input
                new_u_form.first_name = form.cleaned_data.get('first_name')
                new_u_form.last_name = form.cleaned_data.get('last_name')

                new_u_form.save()
                form.save()
                messages.success(request, f'Account has been updated!')    

                return redirect('users:profile')


@login_required
def addresses(request):
    '''update the shipping and billing address of the customer'''
    customer = Customer.objects.filter(user=request.user).first()
    shipping_address = Address.objects.filter(customer=customer, address_type='S',
        default=True).first()
    billing_address = Address.objects.filter(customer=customer, address_type='B',
        default=True).first()

    if request.method == 'GET':
        s_form = ShippingAddressUpdateForm(instance=shipping_address, prefix='shipping')
        b_form = BillingAddressUpdateForm(instance=billing_address, prefix='billing')

        context = {
            's_form': s_form,
            'b_form': b_form,
        }
        return render(request, 'users/addresses.html', context)

    elif request.method == 'POST':
        s_form = ShippingAddressUpdateForm(request.POST, prefix='shipping',
            instance=shipping_address)
        b_form = BillingAddressUpdateForm(request.POST,  prefix='billing',
            instance=billing_address)

        if s_form.is_valid() and b_form.is_valid():
            s_form.save()
            b_form.save()

            messages.success(request, f'Account has been updated!')    
            return redirect('users:addresses')


@login_required
def orders(request):
    customer = Customer.objects.filter(user=request.user).first()
    orders = Order.objects.filter(customer=customer, is_ordered=True)
    if request.method == 'GET':

        context = {
            'orders': orders,
        }
        return render(request, 'users/orders.html', context)


@login_required
def payments(request):
    customer = Customer.objects.filter(user=request.user).first()
    orders = Order.objects.filter(customer=customer, is_ordered=True)
    if request.method == 'GET':

        context = {
            'orders': orders,
        }
        return render(request, 'users/payments.html', context)