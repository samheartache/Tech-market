from django import template
from django.utils.http import urlencode

from cart.models import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def proper_url(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag()
def is_in_cart(product_id, user_id):
    return Cart.objects.filter(product=product_id, user=user_id).exists()