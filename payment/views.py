from ecommerce.models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def stripe(request):
    order = Order.objects.filter(customer=request.user, is_ordered=False).first()
    context = {
        'order': order,
    }
    return render(request, 'payment/stripe.html',context)
