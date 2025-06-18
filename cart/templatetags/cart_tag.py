from django import template
from cart.models import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def user_cart(context):
    request = context['request']
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product')
    return Cart.objects.none()