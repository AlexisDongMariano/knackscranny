from django.contrib import messages
from django.shortcuts import redirect, render


def stripe(request):
    return render(request, 'payment/stripe.html', context)
