from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from app.models.schemas import Earnings, CompletedJob, ApiResponse
from app.routers.auth import get_current_user
from app.services.redis_client import RedisService
import random

router = APIRouter(prefix="/earnings", tags=["earnings"])

# Mock completed jobs data
MOCK_COMPLETED_JOBS = [
    {
        "id": "comp-1",
        "pickup": "123 Main St, Downtown",
        "dropoff": "456 Oak Ave, Uptown", 
        "completed_at": datetime.now() - timedelta(days=1),
        "earnings": 25.50,
        "g_value": 0.75
    },
    {
        "id": "comp-2",
        "pickup": "789 Pine St, Midtown",
        "dropoff": "321 Elm St, Eastside",
        "completed_at": datetime.now() - timedelta(days=2),
        "earnings": 32.00,
        "g_value": 0.68
    },
    {
        "id": "comp-3", 
        "pickup": "555 Broadway, Westside",
        "dropoff": "777 Park Ave, Northside",
        "completed_at": datetime.now() - timedelta(days=3),
        "earnings": 28.75,
        "g_value": 0.82
    },
    {
        "id": "comp-4",
        "pickup": "999 University Blvd, Campus",
        "dropoff": "111 Tech Park, Innovation District",
        "completed_at": datetime.now() - timedelta(days=5),
        "earnings": 35.25,
        "g_value": 0.71
    },
    {
        "id": "comp-5",
        "pickup": "222 Market Square, Old Town", 
        "dropoff": "333 Harbor View, Waterfront",
        "completed_at": datetime.now() - timedelta(days=7),
        "earnings": 42.00,
        "g_value": 0.89
    }
]

@router.get("/", response_model=ApiResponse)
async def get_earnings(current_user: dict = Depends(get_current_user)):
    """Get worker earnings data."""
    try:
        worker_id = current_user.get("user_id", "worker-1")
        cache_key = f"earnings:{worker_id}"
        
        # Check cache first
        cached_earnings = RedisService.get(cache_key)
        if cached_earnings:
            return ApiResponse(data=cached_earnings, message="Earnings retrieved from cache")
        
        # Calculate earnings
        total_earnings = sum(job["earnings"] for job in MOCK_COMPLETED_JOBS)
        
        # Calculate weekly earnings (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        weekly_jobs = [job for job in MOCK_COMPLETED_JOBS if job["completed_at"] >= week_ago]
        weekly_earnings = sum(job["earnings"] for job in weekly_jobs)
        
        # Convert datetime objects to strings for JSON serialization
        completed_jobs = []
        for job in MOCK_COMPLETED_JOBS:
            completed_jobs.append({
                "id": job["id"],
                "pickup": job["pickup"],
                "dropoff": job["dropoff"],
                "completed_at": job["completed_at"].isoformat(),
                "earnings": job["earnings"],
                "g_value": job["g_value"]
            })
        
        earnings_data = {
            "total_earnings": total_earnings,
            "weekly_earnings": weekly_earnings,
            "completed_jobs": completed_jobs
        }
        
        # Cache for 5 minutes
        RedisService.set(cache_key, earnings_data, ttl=300)
        
        return ApiResponse(data=earnings_data, message="Earnings retrieved successfully")
        
    except Exception as e:
        print(f"Error getting earnings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve earnings"
        )
