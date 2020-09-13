from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('stripe/', views.stripe_payment, name='stripe'),
]