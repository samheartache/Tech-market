from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect, render

from products.models import Product
from cart.models import Cart
from cart.utils import get_user_cart

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
    
    product_amount = Cart.objects.get(user=request.user, product=product).quantity
    print(product_amount)
    
    response = {
        'message': 'Товар добавлен в корзину',
        'product_amount': product_amount,
    }

    return JsonResponse(response)


def remove(request):
    product_id = request.POST.get('product_id')
    cart_prod = Cart.objects.get(product=product_id, user=request.user.id)
    cart_prod.delete()

    user_cart = get_user_cart(request=request)
    amount = user_cart.total_quantity()
    price = user_cart.total_price()

    cart_page = render_to_string('includes/empty_cart.html', request=request)

    response = {
        'message': 'Товар удален из корзины',
        'amount': amount,
        'price': f'{price} ₽',
        'cart_page': cart_page,
    }

    return JsonResponse(response)


def decrease(request):
    product_id = request.POST.get('product_id')
    cart_page = render_to_string('includes/empty_cart.html', request=request)

    if request.user.is_authenticated:
        cart_product = Cart.objects.get(user=request.user, product=product_id)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
            product_amount = cart_product.quantity
            response = {
                'product_amount': product_amount,
            }

        else:
            cart_product.delete()
            user_cart = get_user_cart(request=request)
            amount = user_cart.total_quantity()
            response = {
                'product_amount': 0,
                'cart_page': cart_page,
                'amount': amount,
            }

    return JsonResponse(response)

