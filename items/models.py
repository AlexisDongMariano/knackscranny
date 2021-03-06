# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from PIL import Image
from math import floor
from users.models import Customer


ITEM_LABELS = (
    ('NA', 'Not Applicable'),
    ('NW', 'New'),
    ('SD', 'Sold'),
    ('BS', 'Bestseller'),
    ('SL', 'Sale'),
)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    item_label = models.CharField(max_length=2, choices=ITEM_LABELS, default='NA')
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
    
    @property
    def get_review_count(self):
        '''return the review count'''
        return len(self.itemreview_set.all())

    @property
    def get_rating(self):
        '''return the floor average reviews of the item'''
        reviews = self.itemreview_set.all()
        total = floor(sum([review.rating for review in reviews])/len(reviews))
        return total
    
    def image_tag(self):
        '''display the image in admin panel'''
        return mark_safe('<img src="/media/%s" width="100" />' % (self.image))
    
    # column name
    image_tag.short_description = 'Image'


class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='regular')
    alias = models.CharField(max_length=150, blank=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0, blank=True)
    # item_label value is taken from Item but can be overriden unless it's SOLD
    item_label = models.CharField(max_length=2, choices=ITEM_LABELS) 
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
            self.item_label = self.item.item_label
        self.alias = self.item.name + '_' + self.name
        self.date_updated = timezone.now()
        
        if self.item.item_label == 'SD':
            self.item_label = 'SD'
        super(Variation, self).save(*args, **kwargs)
        

class VariationImage(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='default')
    alias = models.CharField(max_length=150, blank=True, unique=True)
    image = image = models.ImageField(default=f'default_variation.png', 
        upload_to='item_variation_pics')
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        ''' On save, update some fields and delete obselete image'''
        #* deletes the previous image when updated
        if VariationImage.objects.filter(id=self.id).exists(): # do if the user/profile exists
            this = VariationImage.objects.filter(id=self.id).first()
            
            if this.image != self.image and this.image != 'default_variation.png':
                this.image.delete(save=False)
                print('IMAGE DELETED')
        #*
        # ''' On save, update name and date_updated'''
        self.alias = self.variation.alias + '_' + self.name
        if not self.id:
            self.date_added = timezone.now()
        self.date_updated = timezone.now()

        super(VariationImage, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 525:
            output_size = (525, 350)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def image_tag(self):
        '''display the image in admin panel'''
        return mark_safe('<img src="/media/%s" width="150" />' % (self.image))
    
    # column name
    image_tag.short_description = 'Image'


class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name

    def save(self, *args, **kwargs):
        ''' On save, update date updated '''
        if not self.id:
            self.date_added = timezone.now()
        self.date_updated = timezone.now()

        super(ItemReview, self).save(*args, **kwargs)