from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('search/', views.get_products, name='search'),
    path('<slug:category_slug>/', views.get_products, name='products'),
    path('product/<slug:product_slug>', views.product, name='product'),
]
