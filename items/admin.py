from django.contrib import admin
from .models import Category, Item, ItemReview, Variation, VariationImage

class ItemAdmin(admin.ModelAdmin):        
    def col_price_discount(self, obj):
        return obj.price_discount
    
    def col_item_label(self, obj):
        return obj.get_item_label_display()
      
    col_price_discount.allow_tags = True
    col_price_discount.short_description = 'discount'
    col_item_label.allow_tags = True
    col_item_label.short_description = 'label'
    col_item_label.admin_order_field = 'item_label'

    list_display = [
        'id',
        'name',
        'category',
        'price',
        'col_price_discount',
        'col_item_label',
        'date_added',
        'date_updated'
    ]

    list_display_links = [
        'id'
    ]

    # list_filter = ['item', 'quantity', 'date_added']
    # search_fields = ['item__item__name', 'item__name', 'order__id', 'ordered_item_price'] 

class VariationAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ['description']

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
# admin.site.register(Item)
admin.site.register(ItemReview)
admin.site.register(Variation, VariationAdmin)
admin.site.register(VariationImage)



