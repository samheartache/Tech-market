from cart.models import Cart

def get_user_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)