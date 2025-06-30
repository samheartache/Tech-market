from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView

from products.utils import query_handler
from products.models import Category, Product


class ProductsView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    slug_url_kwarg = 'category_slug'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        sort_way = self.request.GET.get('sort_way', None)
        query = self.request.GET.get('q', None)

        if category_slug == 'all':
            products = super().get_queryset()
            
        elif query:
            products = query_handler(query)

        else:
            products = super().get_queryset().filter(category__slug=category_slug)
    
        if sort_way and sort_way != 'default':
            products = products.order_by(sort_way)
        
        return products 
        

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'Каталог товаров'
       context['slug'] = self.kwargs.get(self.slug_url_kwarg)
       context['categories'] = Category.objects.all()
       return context



class ProductView(DetailView):
    template_name = 'products/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
        
