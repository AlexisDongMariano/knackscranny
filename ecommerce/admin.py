from django.contrib import admin
from .models import Item, Variation, VariationImage, Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe

class OrderAdmin(admin.ModelAdmin):
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:auth_user_change', args=(obj.customer.id,)), obj.customer
            ))
        user_link.allow_tags = True
        user_link.short_description = 'User'
    
    # def test(self, obj):
    #     return mark_safe('<a href="%s">%s</a>' % (
    #             reverse('admin:address_change', args=(obj.customer.id,)), obj.customer
    #         ))
    #     user_link.allow_tags = True
    #     user_link.short_description = 'User'
    def ship_address(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
            reverse('admin:users_address_change', args=(obj.shipping_address.id,)), obj.shipping_address
            ))
        test.allow_tags = True
        test.short_description = 'address'
    def bill_address(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
            reverse('admin:users_address_change', args=(obj.billing_address.id,)), obj.billing_address
            ))
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
        'user', # refers to the user method above
        'ship_address',
        'bill_address',
        'payment_detail',
        'date_added',
        'is_ordered',
        'ordered_date',
    ]
    list_filter = ['payment', 'is_ordered', 'ordered_date', 'date_added']
    search_fields = ['customer__username', 'shipping_address', 'billing_address'] 

admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(Variation)
admin.site.register(VariationImage)
# admin.site.register(Order)
admin.site.register(OrderItem)


