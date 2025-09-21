from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.schemas import Order, ApiResponse
from app.routers.auth import get_current_user
from app.services.redis_client import RedisService
from app.services.g_value_client import GValueClient
import random
import string

router = APIRouter(prefix="/orders", tags=["orders"])

# Mock orders data
MOCK_ORDERS = [
    {
        "id": "1",
        "pickup": "123 Main St, Downtown",
        "dropoff": "456 Oak Ave, Uptown",
        "eta": 15,
        "status": "available"
    },
    {
        "id": "2", 
        "pickup": "789 Pine St, Midtown",
        "dropoff": "321 Elm St, Eastside",
        "eta": 25,
        "status": "available"
    },
    {
        "id": "3",
        "pickup": "555 Broadway, Westside", 
        "dropoff": "777 Park Ave, Northside",
        "eta": 35,
        "status": "available"
    },
    {
        "id": "4",
        "pickup": "999 University Blvd, Campus",
        "dropoff": "111 Tech Park, Innovation District",
        "eta": 20,
        "status": "available"
    },
    {
        "id": "5",
        "pickup": "222 Market Square, Old Town",
        "dropoff": "333 Harbor View, Waterfront",
        "eta": 30,
        "status": "available"
    }
]

def generate_random_order_id() -> str:
    """Generate a random order ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.get("/", response_model=ApiResponse)
async def get_orders(current_user: dict = Depends(get_current_user)):
    """Get all available orders with G-value predictions."""
    try:
        # Get worker_id first
        worker_id = current_user.get("user_id", "worker-1")
        
        # Check cache first
        cache_key = RedisService.get_orders_cache_key(worker_id)
        cached_orders = RedisService.get(cache_key)
        
        if cached_orders:
            return ApiResponse(data=cached_orders, message="Orders retrieved from cache")
        
        # Generate orders with G-value predictions
        orders_with_g_values = []
        
        for order in MOCK_ORDERS:
            if order["status"] == "available":
                # Get G-value prediction
                features = {
                    "pickup_location": order["pickup"],
                    "dropoff_location": order["dropoff"],
                    "eta": order["eta"],
                    "time_of_day": 14,  # Mock time
                    "day_of_week": 1,   # Mock day
                }
                
                g_value_result = GValueClient.get_g_value_prediction_sync(
                    worker_id, order["id"], features
                )
                
                order_with_g_value = {
                    **order,
                    "g_mean": g_value_result["g_mean"],
                    "g_var": g_value_result["g_var"],
                    "worker_id": None
                }
                orders_with_g_values.append(order_with_g_value)
        
        # Cache the results for 2 minutes
        RedisService.set(cache_key, orders_with_g_values, ttl=120)
        
        return ApiResponse(data=orders_with_g_values, message="Orders retrieved successfully")
        
    except Exception as e:
        print(f"Error getting orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders"
        )

@router.post("/accept/{order_id}", response_model=ApiResponse)
async def accept_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Accept an order."""
    try:
        worker_id = current_user.get("user_id", "worker-1")
        
        # In a real app, this would update the database
        # For now, we'll just invalidate the cache
        cache_key = RedisService.get_orders_cache_key(worker_id)
        RedisService.delete(cache_key)
        
        # Mock response
        return ApiResponse(
            data={"order_id": order_id, "status": "accepted", "worker_id": worker_id},
            message="Order accepted successfully"
        )
        
    except Exception as e:
        print(f"Error accepting order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept order"
        )

@router.post("/complete/{order_id}", response_model=ApiResponse)
async def complete_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Mark an order as complete."""
    try:
        worker_id = current_user.get("user_id", "worker-1")
        
        # In a real app, this would update the database
        # For now, we'll just invalidate the cache
        cache_key = RedisService.get_orders_cache_key(worker_id)
        RedisService.delete(cache_key)
        
        # Mock response
        return ApiResponse(
            data={"order_id": order_id, "status": "completed", "worker_id": worker_id},
            message="Order completed successfully"
        )
        
    except Exception as e:
        print(f"Error completing order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete order"
        )
