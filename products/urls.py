from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('search/', views.ProductsView.as_view(), name='search'),
    path('<slug:category_slug>/', views.ProductsView.as_view(), name='products'),
    path('product/<slug:product_slug>', views.ProductView.as_view(), name='product'),
]
