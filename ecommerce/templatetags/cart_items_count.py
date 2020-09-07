from django import template
from ecommerce.models import Order

register = template.Library()


@register.filter
def cart_items_count(user):
    if user.is_authenticated:
        order = Order.objects.filter(customer=user, is_ordered=False).first()
        return order.get_cart_items
    return 0