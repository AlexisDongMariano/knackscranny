from ecommerce.models import Order, OrderItem
from django.conf import settings as conf_settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
import stripe


stripe.api_key = conf_settings.STRIPE_SECRET_KEY



def stripe_payment(request):
    if request.method == 'GET':
        order = Order.objects.filter(customer=request.user, is_ordered=False).first()
        items = order.orderitem_set.all()
        context = {
            'order': order,
            'items': items,
        }
        return render(request, 'payment/stripe.html',context)

    elif request.method == 'POST':
        print('DATA:', request.POST)
        stripe.Customer.create(
            description="test customer",
            name="Alexis Dong Mariano",
            email="alexisdongmariano@gmail.com"
        )
        stripe.PaymentIntent.create(
            amount=10*100,
            currency='usd',
            payment_method_types=['card'],
            receipt_email='alexisdongmariano@gmail.com',
        )
        
        return redirect('payment:stripe')