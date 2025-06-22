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
    user_cart = get_user_cart(request=request)

    cart_products = Cart.objects.filter(user=request.user, product=product) if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key, product=product)
    if cart_products.exists():
        cart_product = cart_products.first()
        if cart_product:
            cart_product.quantity += 1
            cart_product.save()

            product_amount = cart_product.quantity
            sum_price = cart_product.products_price()
            total_price = user_cart.total_price()

            response = {
                'product_amount': product_amount,
                'sum_price': f'Сумма: {sum_price} ₽',
                'total_price': f'{total_price} ₽',
            }
    else:
        if request.user.is_authenticated:
            Cart.objects.create(user=request.user, product=product, quantity=1)
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

        response = {
            'message': 'Товар добавлен в корзину',
        }
    
    return JsonResponse(response)


def remove(request):
    product_id = request.POST.get('product_id')
    emptycart_page = render_to_string('includes/empty_cart.html', request=request)

    cart_product = Cart.objects.get(product=product_id, user=request.user.id) if request.user.is_authenticated else Cart.objects.get(session_key=request.session.session_key, product=product_id)
    cart_product.delete()

    user_cart = get_user_cart(request=request)
    amount = user_cart.total_quantity()
    total_price = user_cart.total_price()

    response = {
        'message': 'Товар удален из корзины',
        'amount': amount,
        'total_price': f'{total_price} ₽',
        'cart_page': emptycart_page,
    }

    return JsonResponse(response)


def decrease(request):
    product_id = request.POST.get('product_id')
    emptycart_page = render_to_string('includes/empty_cart.html', request=request)
    user_cart = get_user_cart(request=request)

    cart_product = Cart.objects.get(user=request.user, product=product_id) if request.user.is_authenticated else Cart.objects.get(session_key=request.session.session_key, product=product_id)
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()

        product_amount = cart_product.quantity
        sum_price = cart_product.products_price()
        total_price = user_cart.total_price()

        response = {
            'product_amount': product_amount,
            'sum_price': f'Сумма: {sum_price} ₽',
            'total_price': f'{total_price} ₽',
        }

    else:
        cart_product.delete()

        total_price = user_cart.total_price()
        total_amount = user_cart.total_quantity()

        response = {
            'product_amount': 0,
            'cart_page': emptycart_page,
            'total_amount': total_amount,
            'total_price': f'{total_price} ₽',
        }

    return JsonResponse(response)

