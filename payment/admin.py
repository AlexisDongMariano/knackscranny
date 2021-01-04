from .models import Payment, Coupon
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# class CouponAdmin(admin.ModelAdmin):
#     '''This class is implemented to remove deletion of coupons. We can only add coupons and avoid
#     deletions as they are need for reference'''
#     model = Coupon
#     # this will remove the delete selected items in the coupon page
#     actions = None

#     # this will remove the delete button in the detail page of the Coupon
#     def has_delete_permission(self, request, obj=None):
#         return False

class CouponAdmin(admin.ModelAdmin):
    # def variation_detail(self, obj):
    #     return mark_safe('<a href="%s">%s</a>' % (
    #             reverse('admin:items_variation_change', args=(obj.variation.id,)), obj.variation
    #         ))
    
    # def user(self, obj):
    #     return mark_safe('<a href="%s">%s</a>' % (
    #             reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
    #         ))

    # def col_image_tag(self, obj):
    #     return format_html('<img src="{}" width="70" />'.format(obj.image.url))

    def col_code(self, obj):
        return obj.code

    col_code.admin_order_field = 'code'
    col_code.short_description = 'code'

    list_display = [
        'id',
        'col_code',
        'fixed_amount',
        'percent_value',
        'quantity',
        'date_added',
        'date_updated',
        'date_expiration'
    ]

    list_display_links = ['id']

    list_filter = ['date_added', 'date_updated', 'date_expiration']
    search_fields = ['code', 'fixed_amount', 'percent_value', 'quantity']


class PaymentAdmin(admin.ModelAdmin):
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))
    
    def col_charge_id(self, obj):
        return mark_safe('<a href="https://dashboard.stripe.com/">%s</a>' % (obj.charge_id))

    user.short_description = 'customer'
    user.admin_order_field = 'customer'
    
    list_display = [
        'id',
        'user',
        'col_charge_id',
        'amount',
        'payment_method',
        'date_added',
    ]

    list_display_links = ['id']

    list_filter = ['payment_method', 'date_added']
    search_fields = ['customer__user__username', 'customer__user__first_name',
        'customer__user__last_name', 'customer__user__id', 'charge_id',
        'amount', 'payment_method']

admin.site.register(Coupon, CouponAdmin)
admin.site.register(Payment, PaymentAdmin)
