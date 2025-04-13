from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, SearchHeadline

from products.models import Product


def query_handler(query):
    vector = SearchVector('name', 'description')
    query = SearchQuery(query)
    result =  Product.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(rank__gt=0)
    
    result = result.annotate(headline=SearchHeadline('name', query, start_sel='<span style="background_color: yellow;"', stop_sel='</span>')
    return result