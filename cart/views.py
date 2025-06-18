from django.shortcuts import redirect, render

from products.models import Product
from cart.models import Cart

def cart(request):
    context = {
        'title': 'Корзина',
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        Cart.objects.create(user=request.user, product=product, quantity=1)
    return redirect(request.META['HTTP_REFERER'])
