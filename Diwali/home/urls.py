from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('crack/', views.add_products, name='crack'),

    # Add products to common cart
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    # Display cart
    path('cart/', views.cart, name='cart'),

    # Increase and decrease quantity
    path('update-cart/<str:key>/', views.update_cart, name='update_cart'),

    # Remove product
    path('remove-cart/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
]