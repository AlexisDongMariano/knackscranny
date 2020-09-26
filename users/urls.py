from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.customer_page, name='customer-page'),
]