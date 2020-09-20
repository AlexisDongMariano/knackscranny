from django.contrib import admin
from .models import Category, Item, Variation, VariationImage, Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe

class OrderAdmin(admin.ModelAdmin):
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))
        user_link.allow_tags = True
        user_link.short_description = 'customer'
    

    def ship_address(self, obj):
        if obj.shipping_address:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_address_change', args=(obj.shipping_address.id,)), obj.shipping_address
                ))
        else:
            return None
        test.allow_tags = True
        test.short_description = 'address'


    def bill_address(self, obj):
        if obj.billing_address:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_address_change', args=(obj.billing_address.id,)), obj.billing_address
                ))
        else:
            return None
        test.allow_tags = True
        test.short_description = 'address'


    def payment_detail(self, obj):
        if obj.payment:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:payment_payment_change', args=(obj.payment.id,)), obj.payment
                ))
        else:
            return None
        test.allow_tags = True
        test.short_description = 'address'

    list_display = [
        'id',
        'customer',
        'user', # refers to the user method above
        'ship_address',
        'bill_address',
        'payment_detail',
        'coupon',
        'date_added',
        'is_ordered',
        'ordered_date',
    ]
    list_filter = ['payment', 'is_ordered', 'ordered_date', 'date_added', 'coupon']
    search_fields = ['customer__username', 'shipping_address', 'billing_address', 'coupon'] 

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


