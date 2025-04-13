from django.db.models import Q
from django.contrib.postgres.search import SearchVector

from products.models import Product


def query_handler(query):
    return Product.objects.annotate(search=SearchVector('name', 'description')).filter(search=query)