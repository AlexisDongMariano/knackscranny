from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('stripe/', views.stripe_payment, name='stripe'),
    path('add-coupon/', views.add_coupon, name='add-coupon'),
    path('remove-coupon/<int:order_id>', views.remove_coupon, name='remove-coupon'),
]