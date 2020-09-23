from django import template
from ecommerce.models import Order
from ecommerce.views import query_customer

register = template.Library()


# @register.filter
# def cart_items_count(user):
#     if user.is_authenticated:
#         order = Order.objects.filter(customer=user, is_ordered=False)
#         if order.exists():
#             return order.first().get_cart_items
#     return 0

@register.filter
def cart_items_count(request):
    customer = query_customer(request)
    order = Order.objects.filter(customer=customer, is_ordered=False)
    if order.exists():
        return order.first().get_cart_items
    return None
