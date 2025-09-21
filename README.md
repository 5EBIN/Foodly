# Foodly - CN Project Platform

**Foodly – a next-generation food delivery platform that ensures fair wages for workers while minimizing costs for customers through smart algorithms.**

---

## Overview

Foodly is an algorithm-driven food delivery platform designed to improve fairness and efficiency in the delivery ecosystem. It ensures:

- Fair wages for delivery workers
- Optimized delivery costs for customers
- Smart task assignment and routing

This repository contains a **full-stack prototype** featuring React Native mobile app, FastAPI backend, and PyTorch ML service for testing, academic evaluation, and demonstration purposes.

---

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

---

## Features

- **Worker-focused:** Guarantees minimum wages and fair task distribution
- **Customer-focused:** Reduces overall delivery costs
- **Algorithmic efficiency:** Optimized order assignment and delivery routing
- **Mobile app:** React Native frontend for workers
- **ML-powered:** PyTorch + GPyTorch G-value prediction service
- **Real-time:** FastAPI backend with Redis caching

---

## Tech Stack

- **Frontend (Mobile App):** React Native/Expo
- **Backend:** FastAPI + Python
- **ML Service:** PyTorch + GPyTorch
- **Caching:** Redis
- **API Communication:** Axios + React Query
- **Styling:** Tailwind CSS + NativeWind

---

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