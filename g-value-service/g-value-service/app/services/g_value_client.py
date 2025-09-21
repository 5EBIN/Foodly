import httpx
import asyncio
from typing import Dict, Any
from app.services.redis_client import RedisService
import os

G_VALUE_SERVICE_URL = os.getenv("G_VALUE_SERVICE_URL", "http://localhost:5001")

class GValueClient:
    @staticmethod
    async def get_g_value_prediction(worker_id: str, order_id: str, features: Dict[str, Any]) -> Dict[str, float]:
        """Get G-value prediction from the G-value service."""
        cache_key = RedisService.get_g_value_cache_key(worker_id, order_id)
        
        # Check cache first
        cached_result = RedisService.get(cache_key)
        if cached_result:
            return cached_result
        
        # If not in cache, call the G-value service
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{G_VALUE_SERVICE_URL}/predict",
                    json={
                        "worker_id": worker_id,
                        "order_id": order_id,
                        "features": features
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # Cache the result for 5 minutes
                RedisService.set(cache_key, result, ttl=300)
                
                return result
        except Exception as e:
            print(f"G-value service error: {e}")
            # Return mock data if service is unavailable
            return {
                "g_mean": 0.5 + (hash(f"{worker_id}{order_id}") % 50) / 100,  # 0.5-1.0
                "g_var": 0.1 + (hash(f"{order_id}") % 20) / 100  # 0.1-0.3
            }

    @staticmethod
    def get_g_value_prediction_sync(worker_id: str, order_id: str, features: Dict[str, Any]) -> Dict[str, float]:
        """Synchronous wrapper for G-value prediction."""
        return asyncio.run(GValueClient.get_g_value_prediction(worker_id, order_id, features))
