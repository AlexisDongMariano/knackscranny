from .models import Payment
from ecommerce.models import Order, OrderItem
from django.conf import settings as conf_settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
import stripe


stripe.api_key = conf_settings.STRIPE_SECRET_KEY


# process_type 1 = create customer
# process_type 2 = create charge
def stripe_process(request, process_type, stripe_customer=None, amount_total=None):
    '''stripe process of creating customer and charge'''
    error_message = ''
    try:
        if process_type == 1:
            customer = stripe.Customer.create(
                name=request.user.username,
                email=request.user.email,
                source=request.POST.get('stripeToken')
            )
        elif process_type == 2:
            charge = stripe.Charge.create(
                customer=stripe_customer,
                amount=int(amount_total),
                currency='cad',
                receipt_email='alexisdongmariano@gmail.com'
        )     
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        print('Status is: %s' % e.http_status)
        print('Type is: %s' % e.error.type)
        print('Code is: %s' % e.error.code)
        # param is '' in this case
        print('Param is: %s' % e.error.param)
        print('Message is: %s' % e.error.message)
        error_message = e.error.message
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        error_message = 'Too many requests made to the API too quickly'
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        error_message = 'Invalid parameters were supplied to Stripe\'s API'
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        error_message = 'Authentication with Stripe\'s API failed'
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        error_message = 'Network communication with Stripe failed'
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # sendemail.TODO: yourself an email
        error_message = 'Server error. Payment is not made, please try again.'
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        # sendemail.TODO: send email to me
        error_message = e
    else:
        if process_type == 1:
            return [True, customer]
        elif process_type == 2:
            return [True, charge]
    # return error message if an exception has occurred
    return [False, error_message]


def stripe_payment(request):
    '''stripe payment processing'''
    order = Order.objects.filter(customer=request.user, is_ordered=False).first()
    if request.method == 'GET':
        items = order.orderitem_set.all()
        context = {
            'order': order,
            'items': items,
            'STRIPE_PUBLIC_KEY': conf_settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'payment/stripe.html',context)

    elif request.method == 'POST':
        print('DATA:', request.POST)
        amount_total = 10*100 # in cents 

        # create stripe customer
        stripe_customer = stripe_process(request, 1)
        if not stripe_customer[0]:
            messages.error(request, f'Error: {stripe_customer[1]}')
            return redirect('payment:stripe')

        # create stripe charge in canadian dollar
        stripe_charge = stripe_process(request, 2, stripe_customer[1], amount_total)
        if not stripe_charge[0]:
            messages.error(request, f'Error: {stripe_customer[1]}')
            return redirect('payment:stripe')

        try:
            # save the payment in payment model
            payment = Payment()
            payment.customer = request.user
            payment.charge_id = stripe_charge[1]['id']
            payment.amount = amount_total
            payment.payment_method = 'S'
            payment.save()
            
            # update the order to be in ordered state and add the payment
            order.payment = payment
            order.is_ordered = True
            order.ordered_date = timezone.now()
            order.save()
        except Exception as e:
            print(e)
            # 1.TODO: create a charge cancel or charge refund 
            messages.error(request, f'Error: {e}')
            return redirect('payment:stripe')
        else:
            print('transaction and order saving successful')
            # 2.TODO: create a thank you template
            return redirect('ecommerce:home')

        
        
        