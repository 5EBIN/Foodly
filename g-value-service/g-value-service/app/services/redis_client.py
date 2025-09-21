import redis
import json
from typing import Optional, Any
import os

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Create Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

class RedisService:
    @staticmethod
    def set(key: str, value: Any, ttl: int = 300) -> bool:
        """Set a value in Redis with optional TTL."""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return redis_client.setex(key, ttl, value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get a value from Redis."""
        try:
            value = redis_client.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    @staticmethod
    def get_g_value_cache_key(worker_id: str, order_id: str) -> str:
        """Get the cache key for G-value predictions."""
        return f"g_value:{worker_id}:{order_id}"