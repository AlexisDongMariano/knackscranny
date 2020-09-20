from django.contrib import admin
from .models import Category, Item, Variation, VariationImage


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Variation)
admin.site.register(VariationImage)


