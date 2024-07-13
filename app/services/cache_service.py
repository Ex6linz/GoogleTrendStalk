


from functools import lru_cache
import time

class CacheService:
    @staticmethod
    @lru_cache(maxsize=100)
    def get_cached_data(key: str, fetch_function, *args, **kwargs):
        """
        A simple caching decorator that uses lru_cache.

        :param key: A unique key for the cache entry
        :param fetch_function: The function to call if the data is not in the cache
        :param args: Positional arguments for the fetch function
        :param kwargs: Keyword arguments for the fetch function
        :return: The cached or fetched data
        """
        return fetch_function(*args, **kwargs)

    @staticmethod
    def clear_cache():
        """
        Clears the entire cache.
        """
        CacheService.get_cached_data.cache_clear()

    @staticmethod
    def remove_from_cache(key: str):
        """
        Removes a specific entry from the cache.

        :param key: The key of the entry to remove
        """
        CacheService.get_cached_data.cache_delete(key)