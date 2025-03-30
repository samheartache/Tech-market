from django.shortcuts import render
from products.models import Category, Product

def all_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'title': 'Все товары',
        'categories': categories,
        'products': products
    }
    return render(request, 'products/all_products.html', context)
