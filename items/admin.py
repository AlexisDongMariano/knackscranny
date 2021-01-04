from .models import Category, Item, ItemReview, Variation, VariationImage
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ItemAdmin(admin.ModelAdmin):        
    def col_price_discount(self, obj):
        return obj.price_discount
    
    def col_item_label(self, obj):
        return obj.get_item_label_display()
    
    def col_image_tag(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.image.url))
      
    col_price_discount.allow_tags = True
    col_price_discount.short_description = 'discount'
    col_item_label.allow_tags = True
    col_item_label.short_description = 'label'
    col_item_label.admin_order_field = 'item_label'
    col_image_tag.short_description = 'image'

    list_display = [
        'id',
        'name',
        'category',
        'price',
        'col_price_discount',
        'col_item_label',
        'date_added',
        'date_updated',
        # 'image_tag', # this is from Model
        'col_image_tag'
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['category', 'item_label', 'date_added', 'date_updated']
    search_fields = ['name', 'image', 'description'] 
    # fields = ['image_tag']
    # fields += ['image_tag']
    readonly_fields = ['image_tag']


class VariationAdmin(admin.ModelAdmin):
    def item_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:items_item_change', args=(obj.item.id,)), obj.item
            ))
    
    def col_price_discount(self, obj):
        return obj.price_discount
    
    def col_item_label(self, obj):
        return obj.get_item_label_display()

    item_detail.short_description = 'item'
    item_detail.admin_order_field = 'item'
    col_price_discount.short_description = 'discount'
    col_item_label.short_description = 'label'
    col_item_label.admin_order_field = 'item_label'

    list_display = [
        'id',
        'item_detail',
        'name',
        'alias',
        'price',
        'col_price_discount',
        'inventory',
        'col_item_label',
        'active',
        'date_added',
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['item_label', 'active', 'date_added', 'date_updated']
    search_fields = ['item__name', 'name', 'alias', 'price', 'price_discount', 'inventory',
        'description'] 

class VariationImageAdmin(admin.ModelAdmin):
    def variation_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:items_variation_change', args=(obj.variation.id,)), obj.variation
            ))
    
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))

    def col_image_tag(self, obj):
        return format_html('<img src="{}" width="70" />'.format(obj.image.url))

    variation_detail.short_description = 'variation'
    variation_detail.admin_order_field = 'variation'
    col_image_tag.short_description = 'image'

    list_display = [
        'id',
        'variation_detail',
        'name',
        'alias',
        'date_added',
        'date_updated',
        # image_tag is a function in the Model declaration to show the image in Admin
        'col_image_tag'
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['date_added', 'date_updated']
    search_fields = ['variation__alias', 'name', 'alias', 'image']
    readonly_fields = ['image_tag']


class ItemReviewAdmin(admin.ModelAdmin):
    def item_detail(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:items_item_change', args=(obj.item.id,)), obj.item
            ))
    
    def user(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:users_customer_change', args=(obj.customer.id,)), obj.customer
            ))

    item_detail.short_description = 'item'
    item_detail.admin_order_field = 'item'
    user.short_description = 'customer'
    user.admin_order_field = 'customer'

    list_display = [
        'id',
        'item_detail',
        'user',
        'rating',
        'date_added',
        'date_updated'
    ]

    list_display_links = [
        'id'
    ]

    list_filter = ['rating', 'date_added', 'date_updated']
    search_fields = ['item__name', 'customer__user__username', 'customer__user__first_name',
        'customer__user__last_name', 'customer__user__id', 'review'] 


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemReview, ItemReviewAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(VariationImage, VariationImageAdmin)



