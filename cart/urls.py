from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('mycart/', views.cart, name='cart'),
    path('remove/', views.remove, name='remove'),
    path('decrease/', views.decrease, name='decrease')
]