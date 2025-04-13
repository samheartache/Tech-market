from django.db.models import Q

from products.models import Product


def query_handler(query):
    keywords = [word for word in query.split()]
    q_objects = Q()

    for word in keywords:
        q_objects |= Q(name__icontains=word)
        q_objects |= Q(description__contains=word)
    
    return Product.objects.filter(q_objects)