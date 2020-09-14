from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from PIL import Image
from payment.models import Payment
from users.models import Address


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default=f'default.png', upload_to='item_pics')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #* deletes the previous image when updated
        if Item.objects.filter(id=self.id).exists(): # do if the user/profile exists
            this = Item.objects.filter(id=self.id).first()
            
            if this.image != self.image and this.image != 'default.png':
                this.image.delete(save=False)
                print('IMAGE DELETED')
        #*
        if not self.id:
            self.date_added = timezone.now()
        self.date_updated = timezone.now()
        super(Item, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 431 or img.width > 372:
            output_size = (431,372)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='regular')
    alias = models.CharField(max_length=150, blank=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0, blank=True)
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        ''' On save, update fields '''
        if not self.id:
            self.description = self.item.description
            self.date_added = timezone.now()
            self.price = self.item.price
            self.price_discount = self.item.price_discount
        self.alias = self.item.name + '_' + self.name
        self.date_updated = timezone.now()
        super(Variation, self).save(*args, **kwargs)
        

class VariationImage(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='default')
    alias = models.CharField(max_length=150, blank=True, unique=True)
    image = image = models.ImageField(default=f'default_variation.png', upload_to='item_variation_pics')

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        #* deletes the previous image when updated
        if VariationImage.objects.filter(id=self.id).exists(): # do if the user/profile exists
            this = VariationImage.objects.filter(id=self.id).first()
            
            if this.image != self.image and this.image != 'default_variation.png':
                this.image.delete(save=False)
                print('IMAGE DELETED')
        #*
        # ''' On save, update name '''
        self.alias = self.variation.alias + '_' + self.name
        super(VariationImage, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 525:
            output_size = (525, 350)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Order(models.Model):
    '''Basically this is the Cart'''
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # Create a Customer model from Dennis
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True) # add if ordered

    def __str__(self):
        return str(self.id) + '_' + self.customer.username
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total
    
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


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


# might as well put in users app
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name
