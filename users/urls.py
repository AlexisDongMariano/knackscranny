from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.addresses, name='addresses'),
    path('orders/', views.orders, name='orders'),
    path('payments/', views.payments, name='payments'),
]