from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.routers import auth, orders, earnings
from app.models.schemas import HealthResponse
import uvicorn

app = FastAPI(
    title="CN Project Backend API",
    description="Backend API for CN Project worker platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(earnings.router, prefix="/api")

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(status="running", service="backend-api")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="backend-api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
