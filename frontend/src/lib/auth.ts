/**
 * Authentication API Client
 * ==========================
 * 
 * Functions for user authentication and registration.
 * Handles token storage and user session management.
 */

import api from './api';

// TypeScript interfaces
export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    email: string;
    password: string;
    username: string;
    full_name?: string;
}

export interface AuthTokens {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface MFALoginResponse {
    mfa_required: true;
    temp_token: string;
    message: string;
}

export type LoginResponse = AuthTokens | MFALoginResponse;

export interface User {
    id: string;
    email: string;
    username: string;
    full_name?: string;
    is_active: boolean;
    is_superuser: boolean;
    created_at: string;
    updated_at: string;
    role_id?: number;
    role_name?: string;
    role_display_name?: string;
    permissions?: string[];
}

/**
 * Login user with email and password
 * Returns either tokens (if no MFA) or MFA challenge
 */
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/api/v1/auth/login', {
        email: credentials.email,
        password: credentials.password,
    });

    // Check if MFA is required
    if ('mfa_required' in response.data && response.data.mfa_required) {
        // Return MFA challenge - don't store tokens yet
        return response.data;
    }

    // Regular login - store tokens
    const tokens = response.data as AuthTokens;
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);

    return tokens;
};

/**
 * Register a new user
 */
export const register = async (data: RegisterData): Promise<User> => {
    const response = await api.post<User>('/api/v1/auth/register', data);
    return response.data;
};

/**
 * Get current authenticated user
 */
export const getCurrentUser = async (): Promise<User> => {
    const response = await api.get<User>('/api/v1/auth/me');
    return response.data;
};

/**
 * Logout user - clear tokens
 */
export const logout = (): void => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
    if (typeof window === 'undefined') {
        return false; // Server-side rendering
    }
    return !!localStorage.getItem('access_token');
};

/**
 * Get stored access token
 */
export const getAccessToken = (): string | null => {
    if (typeof window === 'undefined') {
        return null; // Server-side rendering
    }
    return localStorage.getItem('access_token');
};
