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
        cart_products = Cart.objects.filter(user=request.user, product=product)
        if cart_products.exists():
            cart_product = cart_products.first()
            if cart_product:
                cart_product.quantity += 1
                cart_product.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    return redirect(request.META['HTTP_REFERER'])


def remove(request, id_in_cart):
    cart_prod = Cart.objects.get(id=id_in_cart)
    cart_prod.delete()
    return redirect(request.META['HTTP_REFERER'])


def decrease(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(user=request.user, product=product)
        cart_product = cart_products.first()
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        else:
            Cart.objects.get(user=request.user, product=product).delete()
    return redirect(request.META['HTTP_REFERER'])

