from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from items.models import Category, Item, Variation, VariationImage
from payment.models import Coupon, Payment
from PIL import Image
from users.models import Address, Customer


class Order(models.Model):
    '''Basically this is the Cart'''
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_subtotal(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total
        
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])

        if self.coupon:
            if self.coupon.fixed_amount:
                total -= self.coupon.fixed_amount
            elif self.coupon.percent_value:
                total = round(total - (total * (self.coupon.percent_value / 100)),2)
        return total
    
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_discount(self):
        if self.coupon.fixed_amount:
            return '-$'+str(self.coupon.fixed_amount)
        elif self.coupon.percent_value:
            # return str(self.coupon.percent_value)[:len(str(self.coupon.percent_value))-3]+'% off'
            return str(round(self.coupon.percent_value,0))+'% off'


class OrderItem(models.Model):
    '''Item/s within the cart'''
    item = models.ForeignKey(Variation, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.alias

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total

