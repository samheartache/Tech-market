from django.shortcuts import render, get_list_or_404
from products.models import Category, Product

def get_products(request, category_slug):
    categories = Category.objects.all()
    if category_slug == 'all':
        products = Product.objects.all()
    else:
        products = get_list_or_404(Product.objects.filter(category__slug=category_slug))
    context = {
        'title': 'Все товары',
        'categories': categories,
        'products': products
    }
    return render(request, 'products/products.html', context)

def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,
        'product': product
    }
    return render(request, 'products/product.html', context)
