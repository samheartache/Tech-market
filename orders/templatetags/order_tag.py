from django import template

from cart.utils import get_user_cart
from orders.utils import get_order_items, get_order_products

register = template.Library()


@register.simple_tag()
def get_order_items_tag(request):
    return get_order_items(request=request)


@register.simple_tag()
def get_order_products_tag(order_id):
    return get_order_products(order_id=order_id)