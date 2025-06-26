from cart.utils import get_user_cart

from orders.models import OrderProduct


def get_order_items(request):
    return get_user_cart(request=request).filter(in_order=True)


def get_order_products(order_id):
    return OrderProduct.objects.filter(order=order_id)