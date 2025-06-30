from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('mycart/', views.CartView.as_view(), name='cart'),
    path('remove/', views.RemoveFromCartView.as_view(), name='remove'),
    path('decrease/', views.DecreaseCartView.as_view(), name='decrease'),
    path('change_order/', views.ChangeOrderItemsView.as_view(), name='change_order'),
    path('select_all/', views.SelectAllInCartView.as_view(), name='select_all'),
]