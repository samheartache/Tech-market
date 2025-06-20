from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, SearchHeadline

from products.models import Product
from cart.models import Cart


def query_handler(query):

    vector = SearchVector('name', 'description')
    query = SearchQuery(query)
    result =  Product.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(rank__gt=0)
    
    result = result.annotate(headline=SearchHeadline('name', query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>'))
    result = result.annotate(bodyline=SearchHeadline('description', query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>'))

    return result
