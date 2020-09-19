from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField



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

    def __str__(self):
        return str(self.id)


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.customer.user:
            return self.customer.user.username + "_" + str(self.id)
        else:
            return 'user' + str(self.customer.id) + str(self.id)

    class Meta:
        verbose_name_plural = 'Addresses'
