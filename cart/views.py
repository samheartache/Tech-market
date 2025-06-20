from django.http import JsonResponse
from django.shortcuts import redirect, render

from products.models import Product
from cart.models import Cart

def cart(request):
    context = {
        'title': 'Корзина',
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(user=request.user, product=product)
        if cart_products.exists():
            cart_product = cart_products.first()
            if cart_product:
                cart_product.quantity += 1
                cart_product.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    
    response = {
        'message': 'Товар добавлен в корзину'
    }

    return JsonResponse(response)


def remove(request):
    product_id = request.POST.get('product_id')
    cart_prod = Cart.objects.get(product=product_id, user=request.user.id)
    cart_prod.delete()

    response = {
        'message': 'Товар удален из корзины'
    }

    return JsonResponse(response)


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

