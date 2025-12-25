'use client';

/**
 * Roles Management Page
 * =====================
 * 
 * Page for viewing and managing roles and permissions.
 */

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import RoleModal from '@/components/roles/RoleModal';
import PermissionMatrix from '@/components/roles/PermissionMatrix';
import { getRoles, RoleListItem, deleteRole, createRole, updateRole, RoleCreate, RoleUpdate } from '@/lib/roles';
import '@/styles/dashboard.css';

export default function RolesPage() {
    const [roles, setRoles] = useState<RoleListItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [view, setView] = useState<'list' | 'matrix'>('list');
    const [search, setSearch] = useState('');
    const [selectedRole, setSelectedRole] = useState<RoleListItem | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

    // Fetch roles
    const fetchRoles = async () => {
        try {
            setLoading(true);
            const data = await getRoles();
            setRoles(data);
        } catch (error: any) {
            console.error('Error fetching roles:', error);
            showNotification('error', 'Failed to load roles');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRoles();
    }, []);

    // Show notification
    const showNotification = (type: 'success' | 'error', message: string) => {
        setNotification({ type, message });
        setTimeout(() => setNotification(null), 3000);
    };

    // Handle create role
    const handleCreateRole = () => {
        setSelectedRole(null);
        setIsModalOpen(true);
    };

    // Handle edit role
    const handleEditRole = (role: RoleListItem) => {
        setSelectedRole(role);
        setIsModalOpen(true);
    };

    // Handle save role
    const handleSaveRole = async (data: RoleCreate | RoleUpdate) => {
        try {
            if (selectedRole) {
                await updateRole(selectedRole.id, data as RoleUpdate);
                showNotification('success', 'Role updated successfully');
            } else {
                await createRole(data as RoleCreate);
                showNotification('success', 'Role created successfully');
            }
            fetchRoles();
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Failed to save role';
            showNotification('error', errorMessage);
            throw error; // Re-throw for RoleModal to handle loading state
        }
    };

    const handleDeleteRole = async (id: number, name: string) => {
        if (!window.confirm(`Are you sure you want to delete the role "${name}"?`)) {
            return;
        }

        try {
            await deleteRole(id);
            showNotification('success', 'Role deleted successfully');
            fetchRoles();
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Failed to delete role';
            showNotification('error', errorMessage);
        }
    };

    // Filter roles based on search
    const filteredRoles = roles.filter(role =>
        role.name.toLowerCase().includes(search.toLowerCase()) ||
        role.display_name.toLowerCase().includes(search.toLowerCase()) ||
        (role.description && role.description.toLowerCase().includes(search.toLowerCase()))
    );

    return (
        <DashboardLayout>
            {/* Notification */}
            {notification && (
                <div style={{
                    position: 'fixed',
                    top: '1rem',
                    right: '1rem',
                    padding: '1rem 1.5rem',
                    background: notification.type === 'success' ? '#34c759' : '#ff3b30',
                    color: '#fff',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    zIndex: 2000,
                }}>
                    {notification.message}
                </div>
            )}

            <div className="card">
                <div className="card-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                        <h3 className="card-title" style={{ margin: 0 }}>Role Management</h3>
                        <div style={{
                            display: 'flex',
                            background: '#f5f5f7',
                            padding: '0.25rem',
                            borderRadius: '8px',
                            gap: '0.25rem'
                        }}>
                            <button
                                onClick={() => setView('list')}
                                style={{
                                    padding: '0.4rem 1rem',
                                    borderRadius: '6px',
                                    border: 'none',
                                    fontSize: '0.75rem',
                                    fontWeight: '600',
                                    cursor: 'pointer',
                                    background: view === 'list' ? '#fff' : 'transparent',
                                    boxShadow: view === 'list' ? '0 2px 4px rgba(0,0,0,0.05)' : 'none',
                                    color: view === 'list' ? '#0071e3' : '#86868b',
                                }}
                            >
                                List View
                            </button>
                            <button
                                onClick={() => setView('matrix')}
                                style={{
                                    padding: '0.4rem 1rem',
                                    borderRadius: '6px',
                                    border: 'none',
                                    fontSize: '0.75rem',
                                    fontWeight: '600',
                                    cursor: 'pointer',
                                    background: view === 'matrix' ? '#fff' : 'transparent',
                                    boxShadow: view === 'matrix' ? '0 2px 4px rgba(0,0,0,0.05)' : 'none',
                                    color: view === 'matrix' ? '#0071e3' : '#86868b',
                                }}
                            >
                                Permission Matrix
                            </button>
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        {view === 'list' && (
                            <input
                                type="text"
                                placeholder="Search roles..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                style={{
                                    padding: '0.5rem 1rem',
                                    border: '1px solid rgba(0,0,0,0.08)',
                                    borderRadius: '8px',
                                    fontSize: '0.875rem',
                                    width: '200px'
                                }}
                            />
                        )}
                        <button
                            className="card-action"
                            style={{ cursor: 'pointer' }}
                            onClick={handleCreateRole}
                        >
                            Create Role +
                        </button>
                    </div>
                </div>

                {view === 'list' ? (
                    loading ? (
                        <div style={{ padding: '2rem', textAlign: 'center', color: '#86868b' }}>
                            Loading roles...
                        </div>
                    ) : (
                        <div className="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Role Name</th>
                                        <th>Display Name</th>
                                        <th>Type</th>
                                        <th>Permissions</th>
                                        <th>Users</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredRoles.map((role) => (
                                        <tr key={role.id}>
                                            <td>
                                                <code style={{
                                                    background: '#f5f5f7',
                                                    padding: '0.2rem 0.4rem',
                                                    borderRadius: '4px',
                                                    fontSize: '0.8rem'
                                                }}>
                                                    {role.name}
                                                </code>
                                            </td>
                                            <td style={{ fontWeight: '500' }}>{role.display_name}</td>
                                            <td>
                                                <span className={`status-badge ${role.is_system_role ? 'status-active' : 'status-inactive'}`} style={{
                                                    background: role.is_system_role ? '#e1f5fe' : '#f5f5f7',
                                                    color: role.is_system_role ? '#01579b' : '#666'
                                                }}>
                                                    {role.is_system_role ? 'System' : 'Custom'}
                                                </span>
                                            </td>
                                            <td>
                                                <span style={{ fontWeight: '600', color: '#0071e3' }}>
                                                    {role.permission_count}
                                                </span>
                                            </td>
                                            <td>{role.user_count}</td>
                                            <td>
                                                <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                    <button
                                                        onClick={() => handleEditRole(role)}
                                                        style={{
                                                            padding: '0.25rem 0.75rem',
                                                            fontSize: '0.75rem',
                                                            background: '#f5f5f7',
                                                            border: 'none',
                                                            borderRadius: '6px',
                                                            cursor: 'pointer',
                                                            color: '#0071e3',
                                                            fontWeight: '600',
                                                        }}
                                                    >
                                                        {role.is_system_role ? 'View' : 'Manage'}
                                                    </button>
                                                    {!role.is_system_role && (
                                                        <button
                                                            onClick={() => handleDeleteRole(role.id, role.display_name)}
                                                            style={{
                                                                padding: '0.25rem 0.75rem',
                                                                fontSize: '0.75rem',
                                                                background: '#f5f5f7',
                                                                border: 'none',
                                                                borderRadius: '6px',
                                                                cursor: 'pointer',
                                                                color: '#ff3b30',
                                                                fontWeight: '600',
                                                            }}
                                                        >
                                                            Delete
                                                        </button>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )
                ) : (
                    <PermissionMatrix />
                )}
            </div>

            <RoleModal
                role={selectedRole}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSave={handleSaveRole}
            />
        </DashboardLayout>
    );
}
