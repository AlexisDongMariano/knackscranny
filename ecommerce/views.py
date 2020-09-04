from django.contrib import messages
from django.db.models import F
from django.shortcuts import redirect, render
from .models import Item, Variation, VariationImage, Order, OrderItem


def home(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'ecommerce/home.html', context)


def item(request, item_id, variation_name):
    '''item details and variations'''
    item = Item.objects.filter(id=item_id).first()
    variation = Variation.objects.filter(item=item, name=variation_name).first()
    variation_images = VariationImage.objects.filter(variation=variation)
    variations = Variation.objects.filter(item=item)

    context = {
        'variation': variation,
        'variation_images': variation_images,
        'variations': variations,
    }
    return render(request, 'ecommerce/item.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user #request.user.customer in dennis
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
 
    context = {
        'items': items,
        'order': order,
        }
    return render(request, 'ecommerce/cart.html', context)


# view_type 1: from item view
# view_type 2: from cart view
def add_to_cart(request, variation_id, view_type):
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        item_inventory = item.inventory

        if item_inventory <= 0:
            messages.error(request, 'Sorry, this item is out of stock. You may go to contact us for item requests.')
        else:
            if request.user.is_authenticated:
                customer = request.user #request.user.customer in dennis
                order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
                order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

                print('item_inventory:', item_inventory)
                print('order item_quantity:', order_item.quantity)
                print(item_inventory - (order_item.quantity + 1))
                if item_inventory < (order_item.quantity + 1):
                    messages.error(request, f'Only {item_inventory} stock(s) left for this item. You may go to contact us for item requests.')
                else:
                    order_item.quantity = F('quantity')+1
                    order_item.save()

                    if created:
                        messages.info(request, 'Item is successfully added! Review cart for more details.')
                    else:
                        messages.info(request, 'Item quantity is updated! Review cart for more details.')

        if view_type == 1:
            return redirect('ecommerce:item', item.item.id, item.name)
        elif view_type == 2:
            return redirect('ecommerce:cart')


def minus_from_cart(request, variation_id):
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        if request.user.is_authenticated:
            customer = request.user #request.user.customer in dennis
            order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

            if order_item.quantity > 1:
                order_item.quantity = F('quantity')-1
                order_item.save()
                messages.info(request, 'Item quantity is updated!')
            else:
                order_item.delete()
                messages.warning(request, 'Item is removed from the cart!')
            
        return redirect('ecommerce:cart')


def delete_cart_item(request, variation_id):
    if request.method == 'POST':
        item = Variation.objects.filter(id=variation_id).first()
        if request.user.is_authenticated:
            customer = request.user #request.user.customer in dennis
            order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
            order_item.delete()
            messages.warning(request, 'Item is removed from the cart!')
            
        return redirect('ecommerce:cart')


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user #request.user.customer in dennis
        order, created = Order.objects.get_or_create(customer=customer, is_ordered=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
 
    context = {
        'items': items,
        'order': order,
        }
    return render(request, 'ecommerce/checkout.html', context)


