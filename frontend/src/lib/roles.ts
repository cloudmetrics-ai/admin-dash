/**
 * Roles API Client
 * ================
 * 
 * Client-side service for managing roles and permissions.
 */

import api from './api';

export interface Permission {
    id: number;
    name: string;
    category: string;
    action: string;
    description: string | null;
}

export interface PermissionsByCategory {
    category: string;
    permissions: Permission[];
}

export interface Role {
    id: number;
    name: string;
    display_name: string;
    description: string | null;
    is_system_role: boolean;
    created_at: string;
    updated_at: string;
    permissions: Permission[];
    user_count?: number;
}

export interface RoleListItem {
    id: number;
    name: string;
    display_name: string;
    description: string | null;
    is_system_role: boolean;
    permission_count: number;
    user_count: number;
}

export interface RoleCreate {
    name: string;
    display_name: string;
    description?: string;
}

export interface RoleUpdate {
    display_name?: string;
    description?: string;
}

/**
 * Get all roles
 */
export const getRoles = async (): Promise<RoleListItem[]> => {
    const response = await api.get<RoleListItem[]>('/api/v1/roles');
    return response.data;
};

/**
 * Get single role by ID
 */
export const getRole = async (roleId: number): Promise<Role> => {
    const response = await api.get<Role>(`/api/v1/roles/${roleId}`);
    return response.data;
};

/**
 * Create a new custom role
 */
export const createRole = async (data: RoleCreate): Promise<Role> => {
    const response = await api.post<Role>('/api/v1/roles', data);
    return response.data;
};

/**
 * Update an existing role
 */
export const updateRole = async (roleId: number, data: RoleUpdate): Promise<Role> => {
    const response = await api.put<Role>(`/api/v1/roles/${roleId}`, data);
    return response.data;
};

/**
 * Delete a custom role
 */
export const deleteRole = async (roleId: number): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/api/v1/roles/${roleId}`);
    return response.data;
};

/**
 * Assign permissions to a role
 */
export const assignRolePermissions = async (roleId: number, permissionIds: number[]): Promise<Role> => {
    const response = await api.post<Role>(`/api/v1/roles/${roleId}/permissions`, {
        permission_ids: permissionIds
    });
    return response.data;
};

/**
 * Get all available permissions grouped by category
 */
export const getPermissions = async (): Promise<PermissionsByCategory[]> => {
    const response = await api.get<PermissionsByCategory[]>('/api/v1/roles/permissions/all');
    return response.data;
};

/**
 * Assign a role to a user
 */
export const assignUserRole = async (userId: string, roleId: number): Promise<any> => {
    const response = await api.patch(`/api/v1/users/${userId}/role`, {
        role_id: roleId
    });
    return response.data;
};
