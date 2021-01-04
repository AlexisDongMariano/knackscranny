from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from PIL import Image


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    session_id = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    contact1 = models.CharField(max_length=30, blank=True, null=True)
    contact2 = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default=f'default_profile.png', upload_to='profile_pics')

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        #* deletes the previous image when updated
        if Customer.objects.filter(id=self.id).exists():
            this = Customer.objects.filter(id=self.id).first()
            
            if this.image != self.image and this.image != 'default_profile.png':
                this.image.delete(save=False)
                print('IMAGE DELETED')
        #*
        self.date_updated = timezone.now()
        super(Customer, self).save(*args, **kwargs)
        # super().save(*args, **kwargs) #old save
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def image_tag(self):
        '''display the image in admin panel'''
        return mark_safe('<img src="/media/%s" width="100" />' % (self.image))
    
    # column name
    image_tag.short_description = 'Image'


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.customer.user:
            return self.customer.user.username + "_" + str(self.id)
        else:
            return 'user' + str(self.customer.id) + "_" + str(self.id)

    class Meta:
        verbose_name_plural = 'Addresses'

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super(Address, self).save(*args, **kwargs)
