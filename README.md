# CN Project - Foodly Platform

A full-stack gadget-selling/work4food-style matching platform prototype featuring:

- **React Native/Expo** worker mobile app
- **FastAPI** backend API
- **PyTorch + GPyTorch** G-value prediction service
- **Redis** caching layer
- **Axios + React Query** for API communication

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Redis (optional, falls back to mock data)

### Installation

1. **Install all dependencies:**
   ```bash
   npm run install:all
   ```

2. **Start all services:**
   ```bash
   # Terminal 1 - Backend API
   npm run start:backend
   
   # Terminal 2 - G-value Service
   npm run start:gvalue
   
   # Terminal 3 - Frontend
   npm run start:frontend
   ```

### Services

- **Frontend**: http://localhost:8081 (Expo)
- **Backend API**: http://localhost:8000
- **G-value Service**: http://localhost:5001

## 📱 Mobile App Features

- **Authentication**: Login/Registration (demo mode - any credentials work)
- **Orders**: View available jobs with ML-predicted G-values
- **Current Job**: Track active assignments
- **Earnings**: View completed jobs and earnings

## 🔧 Backend API Endpoints

- `POST /api/auth/login` - User authentication
- `GET /api/orders` - Get available orders with G-values
- `POST /api/orders/accept/{order_id}` - Accept an order
- `POST /api/orders/complete/{order_id}` - Complete an order
- `GET /api/earnings` - Get worker earnings

## 🤖 G-value Service

- `POST /predict` - Predict G-value for worker-order combination
- `POST /train` - Manually trigger model training
- `GET /health` - Health check

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Native  │    │   FastAPI       │    │   G-value       │
│   Mobile App    │◄──►│   Backend       │◄──►│   Service       │
│   (Expo)        │    │   (Port 8000)   │    │   (Port 5001)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Optional)    │
                       └─────────────────┘
```

## 🧪 Demo Mode

The platform runs in demo mode where:
- Any email/password combination works for login
- Registration automatically logs you in
- Mock data is used for orders and G-value predictions
- No Redis required (falls back to mock predictions)

## 📦 Project Structure

```
cnproject/
├── frontend/worker-app/     # React Native mobile app
├── backend/                 # FastAPI backend
├── g-value-service/         # PyTorch ML service
├── app/                     # Shared models and services
└── package.json            # Root package scripts
```

## 🔬 Machine Learning

The G-value service uses Gaussian Process Regression to predict the value of worker-order combinations based on:
- Pickup/dropoff locations
- Estimated time of arrival
- Time of day and day of week
- Distance estimation

## 📄 License

MIT License - CN Project Team