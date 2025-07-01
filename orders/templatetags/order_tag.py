from django import template

from cart.utils import get_user_cart
from orders.utils import get_order_items, get_order_products
from products.models import Product

register = template.Library()


@register.simple_tag()
def get_order_items_tag(request):
    return get_order_items(request=request)


@register.simple_tag()
def get_order_products_tag(order_id):
    return get_order_products(order_id=order_id)


@register.simple_tag()
def is_single_order(request):
    return True if request.resolver_match.kwargs.get('product_id') else False


@register.simple_tag()
def get_single_order(request):
    single_product_id = request.resolver_match.kwargs.get('product_id')
    product = Product.objects.get(id=single_product_id)
    return product
    