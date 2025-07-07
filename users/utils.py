from users.models import ViewHistory

def get_viewed_products(request):
    return ViewHistory.objects.filter(user=request.user).select_related('product')