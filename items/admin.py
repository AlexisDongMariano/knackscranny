from django.contrib import admin
from .models import Category, Item, ItemReview, Variation, VariationImage


class VariationAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ['description']

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemReview)
admin.site.register(Variation, VariationAdmin)
admin.site.register(VariationImage)



