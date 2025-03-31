from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator
from products.models import Category, Product


def get_products(request, category_slug):

    page = request.GET.get('page', 1)
    sort_way = request.GET.get('sort_way', None)

    categories = Category.objects.all()

    if category_slug == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__slug=category_slug)
    
    if sort_way and sort_way != 'default':
        products = products.order_by(sort_way)

    paginator = Paginator(products, 6)
    current_page = paginator.page(page)

    context = {
        'title': 'Все товары',
        'categories': categories,
        'products': current_page,
        'slug': category_slug,
    }
    return render(request, 'products/products.html', context)


def product(request, product_slug):

    product = Product.objects.get(slug=product_slug)

    context = {
        'title': product.name,
        'product': product
    }
    return render(request, 'products/product.html', context)
