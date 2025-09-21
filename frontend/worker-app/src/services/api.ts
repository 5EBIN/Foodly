import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LoginRequest, LoginResponse, Order, Earnings, ApiResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, clear storage and redirect to login
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await api.post<ApiResponse<LoginResponse>>('/login', credentials);
      const { token, user } = response.data.data;
      
      // Store token and user data
      await AsyncStorage.setItem('auth_token', token);
      await AsyncStorage.setItem('user', JSON.stringify(user));
      
      return { token, user };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  async logout(): Promise<void> {
    await AsyncStorage.removeItem('auth_token');
    await AsyncStorage.removeItem('user');
  },

  async getStoredUser(): Promise<any> {
    const userStr = await AsyncStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  async getStoredToken(): Promise<string | null> {
    return await AsyncStorage.getItem('auth_token');
  }
};

export const orderService = {
  async getOrders(): Promise<Order[]> {
    try {
      const response = await api.get<ApiResponse<Order[]>>('/orders');
      return response.data.data;
    } catch (error) {
      console.error('Get orders error:', error);
      // Return mock data if API fails
      return getMockOrders();
    }
  },

  async acceptOrder(orderId: string): Promise<void> {
    try {
      await api.post(`/accept/${orderId}`);
    } catch (error) {
      console.error('Accept order error:', error);
      throw error;
    }
  },

  async completeOrder(orderId: string): Promise<void> {
    try {
      await api.post(`/complete/${orderId}`);
    } catch (error) {
      console.error('Complete order error:', error);
      throw error;
    }
  }
};

export const earningsService = {
  async getEarnings(): Promise<Earnings> {
    try {
      const response = await api.get<ApiResponse<Earnings>>('/earnings');
      return response.data.data;
    } catch (error) {
      console.error('Get earnings error:', error);
      // Return mock data if API fails
      return getMockEarnings();
    }
  }
};

// Mock data for offline testing
function getMockOrders(): Order[] {
  return [
    {
      id: '1',
      pickup: '123 Main St, Downtown',
      dropoff: '456 Oak Ave, Uptown',
      eta: 15,
      g_mean: 0.75,
      g_var: 0.12,
      status: 'available'
    },
    {
      id: '2',
      pickup: '789 Pine St, Midtown',
      dropoff: '321 Elm St, Eastside',
      eta: 25,
      g_mean: 0.68,
      g_var: 0.15,
      status: 'available'
    },
    {
      id: '3',
      pickup: '555 Broadway, Westside',
      dropoff: '777 Park Ave, Northside',
      eta: 35,
      g_mean: 0.82,
      g_var: 0.08,
      status: 'available'
    }
  ];
}

function getMockEarnings(): Earnings {
  return {
    totalEarnings: 1250.50,
    weeklyEarnings: 320.75,
    completedJobs: [
      {
        id: '1',
        pickup: '123 Main St',
        dropoff: '456 Oak Ave',
        completedAt: '2024-01-15T10:30:00Z',
        earnings: 25.50,
        g_value: 0.75
      },
      {
        id: '2',
        pickup: '789 Pine St',
        dropoff: '321 Elm St',
        completedAt: '2024-01-14T14:20:00Z',
        earnings: 32.00,
        g_value: 0.68
      }
    ]
  };
}
