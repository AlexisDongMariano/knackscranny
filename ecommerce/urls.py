from django.urls import path
from . import views

app_name = 'ecommerce'
urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:item_id>/<str:variation_name>/', views.item, name='item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:variation_id>/<int:view_type>', views.add_to_cart, name='add-to-cart'),
    path('minus-from-cart/<int:variation_id>', views.minus_from_cart, name='minus-from-cart'),
    path('delete-cart-item/<int:variation_id>', views.delete_cart_item, name='delete-cart-item'),
    
]