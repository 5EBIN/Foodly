export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Order {
  id: string;
  pickup: string;
  dropoff: string;
  eta: number; // in minutes
  g_mean: number;
  g_var: number;
  status: 'available' | 'accepted' | 'completed';
  workerId?: string;
}

export interface Earnings {
  totalEarnings: number;
  weeklyEarnings: number;
  completedJobs: CompletedJob[];
}

export interface CompletedJob {
  id: string;
  pickup: string;
  dropoff: string;
  completedAt: string;
  earnings: number;
  g_value: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}
