from django import template

from cart.utils import get_user_cart

register = template.Library()


@register.simple_tag()
def get_order_items(request):
    return get_user_cart(request=request).filter(in_order=True)