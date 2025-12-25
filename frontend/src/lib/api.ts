/**
 * API Client Configuration
 * ========================
 * 
 * Centralized Axios instance for making API requests to the backend.
 * Includes automatic token injection and error handling.
 */

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - Add auth token to requests
api.interceptors.request.use(
    (config) => {
        // Get token from localStorage
        const token = localStorage.getItem('access_token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Handle 401 Unauthorized - token expired or invalid
        // Handle 403 Forbidden - no token or insufficient permissions
        if (error.response?.status === 401 || error.response?.status === 403) {
            // Clear tokens
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');

            // Redirect to login if not already there
            if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
                console.warn('Authentication required. Redirecting to login...');
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default api;
