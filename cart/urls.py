from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('mycart/', views.cart, name='cart'),
    path('remove/', views.remove, name='remove'),
    path('decrease/', views.decrease, name='decrease'),
    path('change_order/', views.change_order, name='change_order'),
    path('select_all/', views.select_all, name='select_all'),
]