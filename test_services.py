#!/usr/bin/env python3
"""
Test script to verify all CN Project services are working correctly.
"""

import requests
import json
import time
import sys

# Service URLs
BACKEND_URL = "http://localhost:8000"
G_VALUE_URL = "http://localhost:5001"

def test_g_value_service():
    """Test the G-value service."""
    print("Testing G-Value Service...")
    
    try:
        # Health check
        response = requests.get(f"{G_VALUE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ G-Value Service health check passed")
        else:
            print("✗ G-Value Service health check failed")
            return False
        
        # Test prediction
        test_request = {
            "worker_id": "test-worker-1",
            "order_id": "test-order-1",
            "features": {
                "pickup_location": "123 Main St, Downtown",
                "dropoff_location": "456 Oak Ave, Uptown",
                "eta": 15,
                "time_of_day": 14,
                "day_of_week": 1
            }
        }
        
        response = requests.post(f"{G_VALUE_URL}/predict", json=test_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ G-Value prediction successful: mean={result['g_mean']:.3f}, var={result['g_var']:.3f}")
            return True
        else:
            print(f"✗ G-Value prediction failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ G-Value Service connection failed: {e}")
        return False

def test_backend_api():
    """Test the backend API."""
    print("\nTesting Backend API...")
    
    try:
        # Health check
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend API health check passed")
        else:
            print("✗ Backend API health check failed")
            return False
        
        # Test login
        login_request = {
            "email": "worker@example.com",
            "password": "password123"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_request, timeout=5)
        if response.status_code == 200:
            result = response.json()
            token = result["data"]["token"]
            print("✓ Login successful")
        else:
            print(f"✗ Login failed: {response.status_code}")
            return False
        
        # Test orders endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/api/orders", headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            orders = result["data"]
            print(f"✓ Orders retrieved successfully: {len(orders)} orders")
        else:
            print(f"✗ Orders retrieval failed: {response.status_code}")
            return False
        
        # Test earnings endpoint
        response = requests.get(f"{BACKEND_URL}/api/earnings", headers=headers, timeout=5)
        if response.status_code == 200:
            result = response.json()
            earnings = result["data"]
            print(f"✓ Earnings retrieved successfully: ${earnings['total_earnings']:.2f} total")
        else:
            print(f"✗ Earnings retrieval failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Backend API connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("CN Project Service Tests")
    print("=" * 40)
    
    # Wait a moment for services to start
    print("Waiting 3 seconds for services to initialize...")
    time.sleep(3)
    
    g_value_ok = test_g_value_service()
    backend_ok = test_backend_api()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"G-Value Service: {'✓ PASS' if g_value_ok else '✗ FAIL'}")
    print(f"Backend API: {'✓ PASS' if backend_ok else '✗ FAIL'}")
    
    if g_value_ok and backend_ok:
        print("\n🎉 All services are working correctly!")
        print("You can now start the React Native app and test the full workflow.")
        return 0
    else:
        print("\n❌ Some services failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
