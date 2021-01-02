from django.contrib import admin
from .models import Payment, Coupon

class CouponAdmin(admin.ModelAdmin):
    '''This class is implemented to remove deletion of coupons. We can only add coupons and avoid
    deletions as they are need for reference'''
    model = Coupon
    # this will remove the delete selected items in the coupon page
    actions = None

    # this will remove the delete button in the detail page of the Coupon
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Payment)
admin.site.register(Coupon, CouponAdmin)
