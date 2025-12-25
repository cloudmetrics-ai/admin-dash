/**
 * API Client Configuration
 * =========================
 * 
 * This module provides a configured Axios instance for making API requests
 * to the FastAPI backend. It includes:
 * - Base URL configuration
 * - Request interceptors (for adding auth tokens)
 * - Response interceptors (for handling errors)
 * - Type-safe API methods
 * 
 * Usage:
 *   import { api } from '@/lib/api';
 *   const response = await api.get('/users');
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

// ============================================================================
// API CLIENT CONFIGURATION
// ============================================================================

/**
 * Create an Axios instance with base configuration
 * 
 * The base URL is loaded from environment variables.
 * In development: http://localhost:8000
 * In production: Your deployed backend URL
 */
const api: AxiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 30000, // 30 seconds timeout
    headers: {
        'Content-Type': 'application/json',
    },
});

// ============================================================================
// REQUEST INTERCEPTOR
// ============================================================================

/**
 * Request interceptor
 * 
 * Automatically adds the JWT token to all requests if available.
 * The token is retrieved from localStorage and added to the Authorization header.
 * 
 * Format: Authorization: Bearer <token>
 */
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // Get token from localStorage
        // In a real app, you might want to use a more secure storage method
        const token = localStorage.getItem('access_token');

        // Add token to headers if it exists
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error: AxiosError) => {
        // Handle request errors
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// ============================================================================
// RESPONSE INTERCEPTOR
// ============================================================================

/**
 * Response interceptor
 * 
 * Handles common response scenarios:
 * - 401 Unauthorized: Token expired, redirect to login
 * - 403 Forbidden: Insufficient permissions
 * - 500 Server Error: Show error message
 * 
 * You can customize this based on your needs.
 */
api.interceptors.response.use(
    (response) => {
        // Return successful responses as-is
        return response;
    },
    async (error: AxiosError) => {
        // Handle response errors
        const status = error.response?.status;

        if (status === 401) {
            // Token expired or invalid
            // Clear stored tokens
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');

            // Redirect to login page
            // Only redirect if not already on login page
            if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        } else if (status === 403) {
            // Insufficient permissions
            console.error('Forbidden: Insufficient permissions');
        } else if (status === 500) {
            // Server error
            console.error('Server error:', error.response?.data);
        }

        return Promise.reject(error);
    }
);

// ============================================================================
// API METHODS
// ============================================================================

/**
 * Authentication API methods
 */
export const authApi = {
    /**
     * Register a new user
     * 
     * @param data - User registration data
     * @returns Promise with user data
     * 
     * Example:
     *   const user = await authApi.register({
     *     email: 'john@example.com',
     *     password: 'SecurePass123',
     *     username: 'johndoe',
     *     full_name: 'John Doe'
     *   });
     */
    register: async (data: {
        email: string;
        password: string;
        username?: string;
        full_name?: string;
    }) => {
        const response = await api.post('/api/v1/auth/register', data);
        return response.data;
    },

    /**
     * Login user
     * 
     * @param email - User email
     * @param password - User password
     * @returns Promise with tokens
     * 
     * Example:
     *   const { access_token, refresh_token } = await authApi.login(
     *     'john@example.com',
     *     'SecurePass123'
     *   );
     *   localStorage.setItem('access_token', access_token);
     *   localStorage.setItem('refresh_token', refresh_token);
     */
    login: async (email: string, password: string) => {
        const response = await api.post('/api/v1/auth/login', { email, password });
        return response.data;
    },

    /**
     * Refresh access token
     * 
     * @param refreshToken - Refresh token
     * @returns Promise with new access token
     * 
     * Example:
     *   const refreshToken = localStorage.getItem('refresh_token');
     *   const { access_token } = await authApi.refreshToken(refreshToken);
     *   localStorage.setItem('access_token', access_token);
     */
    refreshToken: async (refreshToken: string) => {
        const response = await api.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
        return response.data;
    },

    /**
     * Get current user information
     * 
     * @returns Promise with user data
     * 
     * Example:
     *   const user = await authApi.getCurrentUser();
     *   console.log(user.email, user.full_name);
     */
    getCurrentUser: async () => {
        const response = await api.get('/api/v1/auth/me');
        return response.data;
    },

    /**
     * Logout user
     * 
     * Clears tokens from localStorage and calls logout endpoint.
     * 
     * Example:
     *   await authApi.logout();
     *   // User is now logged out
     */
    logout: async () => {
        try {
            await api.post('/api/v1/auth/logout');
        } finally {
            // Always clear tokens, even if the API call fails
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    },
};

/**
 * Helper function to check if user is authenticated
 * 
 * @returns boolean indicating if user has a valid token
 * 
 * Example:
 *   if (isAuthenticated()) {
 *     // User is logged in
 *   } else {
 *     // Redirect to login
 *   }
 */
export const isAuthenticated = (): boolean => {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
};

/**
 * Helper function to get stored token
 * 
 * @returns Access token or null
 */
export const getToken = (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
};

// Export the configured API instance as default
export default api;
