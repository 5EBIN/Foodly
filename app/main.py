from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import GValueRequest, GValueResponse, HealthResponse
from app.services.gp_model import gp_predictor
from app.services.redis_client import RedisService
import time

app = FastAPI(
    title="G-Value Service",
    description="Gaussian Process Regression service for G-value predictions",
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

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(status="running", service="g-value-service")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="g-value-service")

@app.post("/predict", response_model=GValueResponse)
async def predict_g_value(request: GValueRequest):
    """Predict G-value for a worker-order combination."""
    try:
        start_time = time.time()
        
        # Check cache first
        cache_key = RedisService.get_g_value_cache_key(request.worker_id, request.order_id)
        cached_result = RedisService.get(cache_key)
        
        if cached_result:
            print(f"Cache hit for {request.worker_id}:{request.order_id}")
            return GValueResponse(**cached_result)
        
        # Make prediction
        g_mean, g_var = gp_predictor.predict(request.features)
        
        # Prepare response
        result = {
            "g_mean": g_mean,
            "g_var": g_var
        }
        
        # Cache the result for 5 minutes
        RedisService.set(cache_key, result, ttl=300)
        
        prediction_time = time.time() - start_time
        print(f"Prediction completed in {prediction_time:.3f}s for {request.worker_id}:{request.order_id}")
        
        return GValueResponse(**result)
        
    except Exception as e:
        print(f"Error in G-value prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict G-value: {str(e)}"
        )

@app.post("/train")
async def train_model():
    """Manually trigger model training."""
    try:
        gp_predictor.train_model()
        return {"message": "Model training completed successfully"}
    except Exception as e:
        print(f"Error training model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to train model: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)