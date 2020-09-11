from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

PAYMENT_METHOD = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer.username
