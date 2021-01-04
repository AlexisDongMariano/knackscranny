from django.contrib import admin
from .models import Address, Customer
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class AddressAdmin(admin.ModelAdmin):
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:auth_user_change', args=(obj.customer.id,)), obj.customer
            ))
        user_link.allow_tags = True
        user_link.short_description = 'User'

    list_display = [
        'id',
        'user', # refers to the user method above
        'address1',
        'address2',
        'country',
        'zip_code',
        'address_type',
        'default',
        'date_updated'
    ]
    list_filter = ['default', 'address_type', 'date_added', 'date_updated', 'country']
    search_fields = ['customer__username', 'address1', 'address2', 'zip_code', 'country'] 
    # **customer is a model instance, so we have to get other field from that, in our case,
    # the User model has the username field


class CustomerAdmin(admin.ModelAdmin): 
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))
    
    def col_image_tag(self, obj):
        return format_html('<img src="{}" width="70" />'.format(obj.image.url))
    
    user.admin_order_field = 'user'
    user.short_description = 'user'

    list_display = [
        'id',
        'user',
        'first_name',
        'last_name',
        'email',
        'contact1',
        'contact2',
        'col_image_tag'
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['date_added', 'date_updated']
    search_fields = ['user__username', 'user__first_name',
        'user__last_name', 'user__id', 'session_id', 'first_name', 'last_name', 'email', 'image',
        'contact1', 'contact2', 'image'] 
    readonly_fields = ['image_tag']


admin.site.register(Address, AddressAdmin)
admin.site.register(Customer, CustomerAdmin)
