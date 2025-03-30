from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('all/', views.all_products, name='all_products'),
    path('product/', views.all_products, name='product'),
]
