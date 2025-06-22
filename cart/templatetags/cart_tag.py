from django import template

from cart.utils import get_user_cart, all_in_order, amount_in_order, price_in_order

register = template.Library()

@register.simple_tag()
def user_cart(request):
    return get_user_cart(request=request)


@register.simple_tag()
def all_in_order_tag(request):
    return all_in_order(request=request)


@register.simple_tag()
def amount_in_order_tag(request):
    return amount_in_order(request=request)

@register.simple_tag()
def price_in_order_tag(request):
    return price_in_order(request=request)
