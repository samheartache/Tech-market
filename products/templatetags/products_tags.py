from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def proper_url(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)