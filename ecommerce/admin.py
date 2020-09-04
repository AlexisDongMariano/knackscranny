from django.contrib import admin
from .models import Item, Variation, VariationImage, Order, OrderItem

admin.site.register(Item)
admin.site.register(Variation)
admin.site.register(VariationImage)
admin.site.register(Order)
admin.site.register(OrderItem)
