from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, Variation


@receiver(post_save, sender=Item)
def update_variation_item_label(sender, instance, **kwargs):
    # variations = Variation.objects.filter(item=instance)
    # item_label = instance.item_label

    # print('TRYING TO UPDATE')
    # for variation in variations:
    #     variation.item_label = item_label
    #     variation.save()
    Variation.objects.filter(item=instance).update(item_label=instance.item_label)
