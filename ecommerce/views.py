from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import redirect, render
from .forms import CheckoutForm, ItemReviewForm
from .models import Order, OrderItem
from items.models import Category, Item, ItemReview, Variation, VariationImage
from payment.forms import CouponForm
from users.models import Address, Customer



def get_session(request, user=None):
    '''get or create anonymous customer through request.session_key'''
    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key
    customer_session, created = Customer.objects.get_or_create(session_id=session_key)

    if created:
        print('NEW ANONYMOUS USER WAS CREATED')
        print('ANONYMOUS SESSION_ID:', customer_session.session_id)
    else:
        print('ANONYMOUS EXiSTS')
        print('ANONYMOUS SESSION_ID:', customer_session.session_id)
        if user and customer_session.user:
            customer_session = Customer(user=user)
            customer_session.save()
    return customer_session


def query_customer(request):
    '''get the customer. User object if logged in else, the create session user'''
    if request.user.is_authenticated:
        return Customer.objects.filter(user=request.user).first()
    else:
        return get_session(request)


def is_field_valid(fields):
    '''server check if the address fields are empty excluding address2'''
    for i in range(len(fields)):
        # let the fields[1] (address2) empty
        if i == 1:
            continue
        else:
            if fields[i] == '':
                return False
    return True


def save_address(customer, address_fields):
    '''saving address to address model but update if the default is set to True'''
    if address_fields[5]:
        values_to_update = {
            'address1': address_fields[0],
            'address2': address_fields[1],
            'country': address_fields[2],
            'zip_code': address_fields[3]
        }
        address, created = Address.objects.update_or_create(
            customer=customer, address_type=address_fields[4], default=True, 
            defaults=values_to_update)
    else:
        address = Address(
            customer = customer,
            address1 = address_fields[0],
            address2 = address_fields[1],
            country = address_fields[2],
            zip_code = address_fields[3],
            address_type = address_fields[4],
            default = address_fields[5]
        )
        address.save()
    return address


def search(q):
    '''return items using the search term (q) from the fields: name, description, and fk category'''
    print('SEARCH ITEM INITIATED')
    return Item.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)
        | Q(category__name__icontains=q)).order_by('-date_updated')


def filter_items(items, filters):
    '''return items filtered by the checkboxes in home'''
    q = Q()
    for label in filters:
        q = q | Q(item_label__icontains=label)
    return items.filter(q)


def paginate(request, items):
    '''Paginate items/elements, show 8 items per page'''
    paginator = Paginator(items, 8)
    page_number = request.GET.get('page')
    print('paginator is called')

    return paginator.get_page(page_number)


def landing_page(request):
    '''Starting landing page'''
    if not request.user.is_authenticated:
        get_session(request)

    return render(request, 'ecommerce/landing-page.html')


# page_type 1: return collection items
# page_type 2: return made to order items
def home(request, page_type=None):
    '''Main Page for the item list'''
    if not request.user.is_authenticated:
        get_session(request)
    print('SESSION_KEY:', request.session.session_key)

    collection_categories = Category.objects.all()
    q = request.GET.get('search')
    filters = request.GET.getlist('filter')

    # get the item queryset and apply search query
    if q:
        items = search(q)
        page_type = 'searched'
    else:
        items = Item.objects.all()
        q = 'Search'

    # apply filter based on query
    items = filter_items(items, filters).order_by('-date_updated')

    # apply pagination
    page_obj = paginate(request, items)

    context = {
        'page_type': page_type,
        'collection_categories': collection_categories,
        'search_placeholder': q,
        'page_obj': page_obj
    }
    return render(request, 'ecommerce/home.html', context)


def item(request, item_id, variation_name):
    '''item details and variations'''
    item = Item.objects.filter(id=item_id).first()
    customer = query_customer(request)
    # sort by latest review add/update
    reviews = ItemReview.objects.filter(item=item).order_by('-date_updated')
    # user_has_reviewed = reviews.filter(customer=customer).exists()
    user_review = reviews.filter(customer=customer)

    if request.method == 'GET':
        review_form = ItemReviewForm(instance=user_review.first())
        variation = Variation.objects.filter(item=item, name=variation_name).first()
        variation_images = VariationImage.objects.filter(variation=variation)
        variations = Variation.objects.filter(item=item)

        other_items = Item.objects.all().exclude(id=item.id)[:3]
        page_obj = paginate(request, reviews)

        context = {
            'variation': variation,
            'variation_images': variation_images,
            'variations': variations,
            'other_items': other_items,
            'review_form': review_form,
            # 'reviews': reviews,
            'page_obj': page_obj,
            # 'user_has_reviewed': user_has_reviewed
            'user_has_reviewed': user_review.exists(),
            'main_item': item
        }

        if user_review.exists():
            context['user_review'] = user_review.first()

    elif request.method == 'POST':
        form = ItemReviewForm(instance=user_review.first(), data=request.POST)
        rating = request.POST.get('rating-value')

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.customer = customer
            new_review.item = item
            new_review.rating = rating
            new_review.save()

        return redirect('ecommerce:item', item_id, variation_name)

    return render(request, 'ecommerce/item.html', context)


def cart(request):
    '''cart items summary view'''
    customer = query_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
    items = order.orderitem_set.all()

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'ecommerce/cart.html', context)


# view_type 1: from item view
# view_type 2: from cart view
def add_to_cart(request, variation_id, view_type):
    '''add to cart functionality'''
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        item_inventory = item.inventory

        if item_inventory <= 0:
            messages.error(request, 'Sorry, this item is out of stock. You may go to contact us \
                for item requests.')
        else:
            customer = query_customer(request)
            order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

            print(item_inventory - (order_item.quantity + 1))
            if item_inventory < (order_item.quantity + 1):
                messages.error(request, f'Only {item_inventory} stock(s) left for this item. \
                    You may go to contact us for item requests.')
            else:
                order_item.quantity = F('quantity')+1
                order_item.save()

                if created:
                    messages.info(request, 'Item is successfully added! Review cart for more \
                        details.')
                else:
                    messages.info(request, 'Item quantity is updated! Review cart for more \
                        details.')

        if view_type == 1:
            return redirect('ecommerce:item', item.item.id, item.name)
        return redirect('ecommerce:cart')


def minus_from_cart(request, variation_id):
    '''decrement 1 from the single item from the cart'''
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        customer = query_customer(request)
        order = Order.objects.filter(customer=customer, is_ordered=False).first()
        order_item = OrderItem.objects.filter(order=order, item=item).first()
        # order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

        print('order:',order.id, 'order_item:',order_item.id)

        if order_item.quantity > 1:
            order_item.quantity = F('quantity')-1
            order_item.save()
            messages.info(request, 'Item quantity is updated!')
        else:
            order_item.delete()
            messages.warning(request, 'Item is removed from the cart!')
        return redirect('ecommerce:cart')


def delete_cart_item(request, variation_id):
    '''delete the item from the cart'''
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        customer = query_customer(request)
        order = Order.objects.filter(customer=customer, is_ordered=False).first()
        order_item = OrderItem.objects.filter(order=order, item=item).first()
        order_item.delete()
        messages.warning(request, 'Item is removed from the cart!')
        return redirect('ecommerce:cart')


def checkout(request):
    '''checkout form'''
    customer = query_customer(request)
    order = Order.objects.filter(customer=customer, is_ordered=False).first()
    print('CUSTOMER ID:', customer.id)
    shipping_address = Address.objects.filter(customer=customer, address_type='S', default=True)
    billing_address = Address.objects.filter(customer=customer, address_type='B', default=True)

    if request.method == 'GET':
        form = CheckoutForm()
        coupon_form = CouponForm()
        items = order.orderitem_set.all()

        if items:
            context = {
                'items': items,
                'order': order,
                'form': form,
                'coupon_form': coupon_form,
                'display_coupon_form': True
            }

            if shipping_address.exists():
                print('SHIPPING ADDRESS EXISTS')
                context['shipping_address'] = shipping_address.first()
            else:
                print('SHIPPING ADDRESS DOES NOT EXISTS')
            if billing_address.exists():
                context['billing_address'] = billing_address.first()
            return render(request, 'ecommerce/checkout.html', context)
        else:
            messages.warning(request, f'You do not have an active order')
            return redirect('ecommerce:cart')

    elif request.method == 'POST':
        form = CheckoutForm(request.POST)
        print('CHECKOUT DATA:', request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            if not customer.user:
                print('SAVING Customer details')
                customer.first_name = form.cleaned_data.get('first_name')
                customer.last_name = form.cleaned_data.get('last_name')
                customer.email = form.cleaned_data.get('email')
                customer.contact1 = form.cleaned_data.get('contact1')
                customer.contact2 = form.cleaned_data.get('contact2')
                customer.save()
                print('Customer details saved')

            # Shipping Address
            same_address = form.cleaned_data.get('chk_same_address')

            # if saved shipping address is checked. Checkbox will only show if the default
            #  shipping address is found
            if form.cleaned_data.get('chk_use_default_shipping'):
                # double checking, might delete this extra check
                if shipping_address.exists():
                    order.shipping_address = shipping_address.first()
                else:
                    messages.error(request, f'Saved shipping address not found!')
                    return redirect('ecommerce:checkout')
            elif not form.cleaned_data.get('chk_use_default_shipping'): 
                shipping_address1 = form.cleaned_data.get('shipping_address1')
                shipping_address2 = form.cleaned_data.get('shipping_address2')
                shipping_country = form.cleaned_data.get('shipping_country')
                shipping_zip_code = form.cleaned_data.get('shipping_zip_code')
                address_type = 'S'
                save_shipping = form.cleaned_data.get('chk_save_shipping_info')
                temp_address = [shipping_address1, shipping_address2, shipping_country, 
                    shipping_zip_code, address_type, save_shipping]

                if not is_field_valid(temp_address):
                    messages.error(request, f'Please fill in shipping details.')
                    return redirect('ecommerce:checkout')
                order.shipping_address = save_address(customer, temp_address)

            order.save()
            print('ORDER WAS SAVED')

            # Billing Address
            save_billing = form.cleaned_data.get('chk_save_billing_info')
            if same_address:
                # billing_address1 = shipping_address.first().address1
                # billing_address2 = shipping_address.first().address2
                # billing_country = shipping_address.first().country
                # billing_zip_code = shipping_address.first().zip_code
                billing_address1 = order.shipping_address.address1
                billing_address2 = order.shipping_address.address2
                billing_country = order.shipping_address.country
                billing_zip_code = order.shipping_address.zip_code
                address_type = 'B'
                temp_address = [billing_address1, billing_address2, billing_country,
                    billing_zip_code, address_type, save_billing]
                order.billing_address = save_address(customer, temp_address)

            # if saved billing address is checked. Checkbox will only show if the
            # default billing address is found
            elif form.cleaned_data.get('chk_use_default_billing'):
                # double checking, might delete this extra check
                if billing_address.exists():
                    order.billing_address = billing_address.first()
                else:
                    messages.error(request, f'Saved shipping address not found!')
                    return redirect('ecommerce:checkout')
            # same address and use saved default billing address are not checked:
            else:
                billing_address1 = form.cleaned_data.get('billing_address1')
                billing_address2 = form.cleaned_data.get('billing_address2')
                billing_country = form.cleaned_data.get('billing_country')
                billing_zip_code = form.cleaned_data.get('billing_zip_code')
                address_type = 'B'
                temp_address = [billing_address1, billing_address2, billing_country,
                    billing_zip_code, address_type, save_billing]

                if not is_field_valid(temp_address):
                    messages.error(request, f'Please fill in billing details.')
                    return redirect('ecommerce:checkout')
                order.billing_address = save_address(customer, temp_address)

            order.save()

            payment_option = form.cleaned_data.get('payment_option')
            if payment_option == 'S':
                return redirect('payment:stripe')
            elif payment_option == 'P':
                return redirect('payment:paypal')
        else:
            messages.error(request, "Error")

        return redirect('ecommerce:checkout')
