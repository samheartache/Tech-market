from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from products.models import Product
from cart.models import Cart
from cart.utils import get_user_cart, all_in_order, price_in_order, amount_in_order


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        return context


class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        cart_products = Cart.objects.filter(user=request.user, product=product) if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key, product=product)
        if cart_products.exists():
            cart_product = cart_products.first()
            if cart_product:
                cart_product.quantity += 1
                cart_product.save()

                product_amount = cart_product.quantity
                sum_price = cart_product.products_price()
                total_price = price_in_order(request=request)
                amount_order = amount_in_order(request=request)

                response = {
                    'product_amount': product_amount,
                    'sum_price': f'Сумма: {sum_price} ₽',
                    'total_price': f'{total_price} ₽',
                    'amount_order': amount_order,
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


class RemoveFromCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        emptycart_page = render_to_string('includes/empty_cart.html', request=request)

        cart_product = Cart.objects.get(product=product_id, user=request.user.id) if request.user.is_authenticated else Cart.objects.get(session_key=request.session.session_key, product=product_id)
        cart_product.delete()

        user_cart = get_user_cart(request=request)
        amount = user_cart.total_quantity()
        total_price = price_in_order(request=request)
        amount_order = amount_in_order(request=request)
        

        response = {
            'message': 'Товар удален из корзины',
            'amount': amount,
            'total_price': f'{total_price} ₽',
            'emptycart_page': emptycart_page,
            'amount_order': amount_order,
        }

        return JsonResponse(response)


class DecreaseCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        emptycart_page = render_to_string('includes/empty_cart.html', request=request)
        user_cart = get_user_cart(request=request)

        cart_product = Cart.objects.get(user=request.user, product=product_id) if request.user.is_authenticated else Cart.objects.get(session_key=request.session.session_key, product=product_id)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()

            product_amount = cart_product.quantity
            sum_price = cart_product.products_price()
            total_price = price_in_order(request=request)

            amount_order = amount_in_order(request=request)

            response = {
                'product_amount': product_amount,
                'sum_price': f'Сумма: {sum_price} ₽',
                'total_price': f'{total_price} ₽',
                'amount_order': amount_order,
            }

        else:
            cart_product.delete()

            total_price = price_in_order(request=request)
            total_amount = user_cart.total_quantity()
            amount_order = amount_in_order(request=request)

            response = {
                'product_amount': 0,
                'cart_page': emptycart_page,
                'total_amount': total_amount,
                'total_price': f'{total_price} ₽',
                'amount_order': amount_order,
            }

        return JsonResponse(response)


class ChangeOrderItemsView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        order_flag = False if request.POST.get('order_flag') == 'false' else True
        cart_product = Cart.objects.get(user=request.user, product=product_id)
        cart_product.in_order = order_flag
        cart_product.save()

        all_flag = all_in_order(request=request)
        total_price = price_in_order(request=request)
        amount_order = amount_in_order(request=request)

        order_button = render_to_string('includes/order_button.html', request=request)

        response = {
            'all_flag': all_flag,
            'total_price': total_price,
            'amount_order': amount_order,
            'order_button': order_button,
        }

        return JsonResponse(response)


class SelectAllInCartView(View):
    def post(self, request):
        flag = False if request.POST.get('flag') == 'false' else True
        order_button = render_to_string('includes/order_button.html', request=request)

        for cart_prod in Cart.objects.filter(user=request.user):
            cart_prod.in_order = flag
            cart_prod.save()
        
        if flag:
            total_price = price_in_order(request=request)
            amount_order = amount_in_order(request=request)

            response = {
                'total_price': total_price,
                'amount_order': amount_order,
                'order_button': order_button,
            }
        else:
            response = {
                'flag': 1,
            }
        
        return JsonResponse(response)