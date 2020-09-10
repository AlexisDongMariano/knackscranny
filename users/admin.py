from django.contrib import admin
from .models import Address
from django.urls import reverse
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
        'date_added'
    ]
    list_filter = ['default', 'address_type', 'date_added', 'country']
    search_fields = ['customer__username', 'address1', 'address2', 'zip_code', 'country'] 
    # **customer is a model instance, so we have to get other field from that, in our case,
    # the User model has the username field

admin.site.register(Address, AddressAdmin)
