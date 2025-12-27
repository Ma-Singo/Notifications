from django.core.cache import cache
from time import time

def is_limited(key: str, limit: int, window: int) -> bool:
    bucket = int(time())  // window
    cache_key = f"rate:{key}:{bucket}"

    count = cache.incr(cache_key)
    if count ==  1:
        cache.expire(cache_key, window)

    return count > limit