/**
 * Users API Client
 * ================
 * 
 * API client functions for user management CRUD operations.
 */

import api from './api';

export interface User {
    id: string; // UUID from backend
    email: string;
    username?: string;
    full_name?: string;
    is_active: boolean;
    is_superuser: boolean;
    created_at: string;
    updated_at: string;
    role_id?: number | null;
    role_display_name?: string | null;
}

export interface UserUpdate {
    email?: string;
    username?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    role_id?: number | null;
}

/**
 * Get list of users with optional filters
 */
export const getUsers = async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
}): Promise<User[]> => {
    const response = await api.get<User[]>('/api/v1/users', { params });
    return response.data;
};

/**
 * Get single user by ID
 */
export const getUser = async (userId: string): Promise<User> => {
    const response = await api.get<User>(`/api/v1/users/${userId}`);
    return response.data;
};

/**
 * Update user
 */
export const updateUser = async (userId: string, data: UserUpdate): Promise<User> => {
    const response = await api.put<User>(`/api/v1/users/${userId}`, data);
    return response.data;
};

/**
 * Delete user
 */
export const deleteUser = async (userId: string): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/api/v1/users/${userId}`);
    return response.data;
};

/**
 * Activate or deactivate user
 */
export const toggleUserStatus = async (userId: string, isActive: boolean): Promise<User> => {
    const response = await api.patch<User>(`/api/v1/users/${userId}/activate`, null, {
        params: { is_active: isActive }
    });
    return response.data;
};

/**
 * Update a user's role
 */
export const updateUserRole = async (userId: string, roleId: number): Promise<User> => {
    const response = await api.patch<User>(`/api/v1/users/${userId}/role`, {
        role_id: roleId
    });
    return response.data;
};
