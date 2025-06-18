from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<slug:product_slug>', views.add_to_cart, name='add_to_cart'),
    path('mycart/', views.cart, name='cart'),
    path('remove/<int:id_in_cart>', views.remove, name='remove')
]