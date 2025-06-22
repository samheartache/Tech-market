from cart.models import Cart

def get_user_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key)


def all_in_order(request):
    return all(prod.in_order for prod in get_user_cart(request=request))


def price_in_order(request):
    return sum(prod.products_price() for prod in get_user_cart(request=request) if prod.in_order)


def amount_in_order(request):
    return sum(prod.quantity for prod in get_user_cart(request=request) if prod.in_order)