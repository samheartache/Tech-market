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

def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,
        'product': product
    }
    return render(request, 'products/product.html', context)
