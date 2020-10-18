from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, Variation


@receiver(post_save, sender=Item)
def update_variation_item_label(sender, instance, **kwargs):
    # variations = Variation.objects.filter(item=instance)
    # print('VARIATIONS:', variations)
    print('TRYING TO UPDATE')
    Variation.objects.get(item=instance).update(item_label=instance.item_label)
    print('update successful!')
