from cart.utils import get_user_cart


def get_order_items(request):
    return get_user_cart(request=request).filter(in_order=True)