import redis
from django.conf import settings


redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

class IdempotencyLock:
    def __init__(self, key, ttl=300):
        self.key = f"idempotency:{key}"
        self.ttl = ttl

    def acquire(self):
        return redis_client.set(self.key, "1", nx=True, ex=self.ttl)
    
    def release(self):
        redis_client.delete(self.key)