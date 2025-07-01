from django.core.cache import cache


class CacheMixin:

    def cache_data(self, query, cache_name, cache_time):
        data = cache.get(cache_name)

        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data