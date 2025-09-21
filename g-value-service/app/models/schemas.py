from pydantic import BaseModel
from typing import Dict, Any, List, Optional

# G-Value Service Schemas
class GValueRequest(BaseModel):
    worker_id: str
    order_id: str
    features: Dict[str, Any]

class GValueResponse(BaseModel):
    g_mean: float
    g_var: float

class HealthResponse(BaseModel):
    status: str
    service: str

# Backend API Schemas
class User(BaseModel):
    id: str
    email: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: User

class Order(BaseModel):
    id: str
    pickup: str
    dropoff: str
    eta: int  # in minutes
    g_mean: float
    g_var: float
    status: str
    worker_id: Optional[str] = None

class CompletedJob(BaseModel):
    id: str
    pickup: str
    dropoff: str
    completed_at: str
    earnings: float
    g_value: float

class Earnings(BaseModel):
    total_earnings: float
    weekly_earnings: float
    completed_jobs: List[CompletedJob]

class ApiResponse(BaseModel):
    data: Any
    message: Optional[str] = None
