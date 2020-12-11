from .forms import CouponForm
from .models import Coupon, Payment
from ecommerce.models import Order, OrderItem, OrderStatus
from ecommerce.views import query_customer
from django.conf import settings as conf_settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
import random
import string
import stripe


stripe.api_key = conf_settings.STRIPE_SECRET_KEY


def generate_reference_code():
    '''generate the order reference code'''
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# process_type 1 = create customer
# process_type 2 = create charge
def stripe_process(request, process_type, stripe_customer=None, amount_total=None):
    '''stripe process of creating customer and charge'''
    error_message = ''

    try:
        if process_type == 1:
            customer = stripe.Customer.create(
                # name=request.user.username,
                # email=request.user.email,
                name=stripe_customer.first_name + ' ' + stripe_customer.last_name,
                email=stripe_customer.email,
                source=request.POST.get('stripeToken')
            )
        elif process_type == 2:
            print('STRIPE_CUSTOMER:', stripe_customer)
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
    customer = query_customer(request)
    order = Order.objects.filter(customer=customer, is_ordered=False).first()
    if request.method == 'GET':
        items = order.orderitem_set.all()

        if items:
            context = {
                'order': order,
                'items': items,
                'STRIPE_PUBLIC_KEY': conf_settings.STRIPE_PUBLIC_KEY
            }
            return render(request, 'payment/stripe.html',context)
        else:
            messages.warning(request, f'You do not have an active order.')
            return redirect('ecommerce:cart')

    elif request.method == 'POST':
        print('DATA:', request.POST)
        amount_total = order.get_cart_total*100 # in cents 

        # create stripe customer
        stripe_customer = stripe_process(request, 1, customer)
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
            payment.customer = customer
            payment.charge_id = stripe_charge[1]['id']
            payment.amount = order.get_cart_total
            payment.payment_method = 'S'
            payment.save()
            
            # update the order to be in ordered state and add the payment
            order.payment = payment
            order.is_ordered = True
            order.ordered_date = timezone.now()
            order.reference_code = generate_reference_code()
            order.save()

            # creating order status model with Processing as default
            order_status = OrderStatus.objects.create(order=order)
        except Exception as e:
            print(e)
            # 1.TODO: create a charge cancel or charge refund 
            messages.error(request, f'Error: {e}')
            return redirect('payment:stripe')
        else:
            messages.info(request, 'Order was successful')
            # 2.TODO: create a thank you template
            return redirect('ecommerce:home')


def check_coupon_validity(coupon_qs, customer):
    '''check the validity of the coupon code
        return types:
        1: success, coupon should be applied
        2: invalid coupon code (code does not exists in the db)
        3: invalid (code already applied)'''

    if coupon_qs.exists():
        # check if the customer already applied the coupon
        customer_orders = Order.objects.filter(customer=customer, is_ordered=True)
        for customer_order in customer_orders:
            # if a coupon existed in the customer orders, refresh the page and inform
            if customer_order.coupon:
                if customer_order.coupon.code:
                    return 3
        return 1
    return 2


@require_POST
def add_coupon(request):
    '''add discount coupon to the order'''
    customer = query_customer(request)
    order = Order.objects.filter(customer=customer, is_ordered=False).first()
    form = CouponForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data.get('code')
        coupon_qs = Coupon.objects.filter(code=code)
        coupon_validity = check_coupon_validity(coupon_qs, customer)

        if coupon_validity == 1:
            order.coupon = coupon_qs.first()
            order.save()
            messages.info(request, f'Promo code successfully applied')
        elif coupon_validity == 2:
            messages.error(request, f'Invalid promo code')
        else:
            messages.error(request, f'You have already used {code} code')
        return redirect('ecommerce:checkout')

    #     if coupon_qs.exists():
    #         # check if the customer already applied the coupon
    #         customer_orders = Order.objects.filter(customer=customer, is_ordered=True)
    #         for customer_order in customer_orders:
    #             # if a coupon existed in the customer orders, refresh the page and inform
    #             if customer_order.coupon:
    #                 if customer_order.coupon.code:
    #                     messages.error(request, f'You have already used {code} code')
    #                     return redirect('ecommerce:checkout')

    #         # save and use the coupon code if it exists and first time use
    #         order.coupon = coupon_qs.first()
    #         order.save()
    #         messages.info(request, f'Promo code successfully applied')
    #     else:
    #         messages.error(request, f'Invalid promo code')
    # return redirect('ecommerce:checkout')
        