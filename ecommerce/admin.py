from django.contrib import admin
from .models import Order, OrderItem, OrderStatus
from django.urls import reverse
from django.utils.safestring import mark_safe

class OrderAdmin(admin.ModelAdmin):
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))

    def ship_address(self, obj):
        if obj.shipping_address:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_address_change', args=(obj.shipping_address.id,)), obj.shipping_address
                ))
        else:
            return None

    def bill_address(self, obj):
        if obj.billing_address:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_address_change', args=(obj.billing_address.id,)), obj.billing_address
                ))
        else:
            return None

    def payment_detail(self, obj):
        if obj.payment:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:payment_payment_change', args=(obj.payment.id,)), obj.payment
                ))
        else:
            return None

    def coupon_detail(self, obj):
        if obj.coupon:
            return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:payment_coupon_change', args=(obj.coupon.id,)), obj.coupon
                ))
        else:
            return None

    user.allow_tags = True
    user.short_description = 'customer'
    user.admin_order_field = 'customer'
    ship_address.allow_tags = True
    ship_address.short_description = 'ship adr'
    bill_address.allow_tags = True
    bill_address.short_description = 'bill adr'
    payment_detail.allow_tags = True
    payment_detail.short_description = 'payment'
    coupon_detail.allow_tags = True
    coupon_detail.short_description = 'coupon'
    
    list_display = [
        'id',
        'user', # refers to the user method above
        'ship_address',
        'bill_address',
        'payment_detail',
        'coupon_detail',
        'date_added',
        'is_ordered',
        'ordered_date',
    ]
    list_display_links = [
        'id'
    ]
    list_filter = ['payment', 'is_ordered', 'ordered_date', 'date_added', 'coupon', 'shipping_address__country']
    search_fields = ['customer__user__username', 'coupon__code', 'shipping_address__address1',
        'shipping_address__address2', 'shipping_address__zip_code', 'billing_address__address1',
        'billing_address__address2', 'billing_address__zip_code']


class OrderItemAdmin(admin.ModelAdmin):
    def item_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:items_item_change', args=(obj.item.id,)), obj.item
            ))
        
    def order_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:ecommerce_order_change', args=(obj.order.id,)), obj.order
            ))
      
    item_detail.allow_tags = True
    item_detail.short_description = 'item'
    item_detail.admin_order_field = 'item'
    order_detail.allow_tags = True
    order_detail.short_description = 'order'
    order_detail.admin_order_field = 'order'

    list_display = [
        'id',
        'item_detail',
        'order_detail',
        'ordered_item_price',
        'quantity',
        'date_added'
 
    ]
    list_display_links = [
        'id'
    ]

    list_filter = ['item', 'quantity', 'date_added']
    search_fields = ['item__item__name', 'item__name', 'order__id', 'ordered_item_price'] 


class OrderStatusAdmin(admin.ModelAdmin):
    def order_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:ecommerce_order_change', args=(obj.order.id,)), obj.order
            ))
    
    def col_status(self, obj):
        return obj.get_status_display()
      
    order_detail.allow_tags = True
    order_detail.short_description = 'order'
    order_detail.admin_order_field = 'order'
    col_status.short_description = 'status'
    col_status.admin_order_field = 'status'

    list_display = [
        'id',
        'order_detail',
        'col_status',
        'refund_requested',
        'refund_granted',
        'date_added',
        'date_updated'
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['status', 'date_added', 'date_updated', 'refund_requested', 'refund_granted']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)


