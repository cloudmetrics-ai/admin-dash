/**
 * Users Management Page
 * =====================
 * 
 * Complete users management with CRUD operations.
 */

'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import UserModal from '@/components/users/UserModal';
import DeleteConfirmModal from '@/components/users/DeleteConfirmModal';
import { getUsers, updateUser, deleteUser, toggleUserStatus, User, UserUpdate } from '@/lib/users';
import '../../../styles/dashboard.css';

export default function UsersPage() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [selectedUser, setSelectedUser] = useState<User | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [userToDelete, setUserToDelete] = useState<User | null>(null);
    const [deleteLoading, setDeleteLoading] = useState(false);
    const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

    // Fetch users
    const fetchUsers = async () => {
        try {
            setLoading(true);
            const data = await getUsers({ search: search || undefined });
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
            showNotification('error', 'Failed to load users');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, [search]);

    // Show notification
    const showNotification = (type: 'success' | 'error', message: string) => {
        setNotification({ type, message });
        setTimeout(() => setNotification(null), 3000);
    };

    // Handle create user
    const handleCreateUser = () => {
        setSelectedUser(null);
        setIsModalOpen(true);
    };

    // Handle edit user
    const handleEditUser = (user: User) => {
        setSelectedUser(user);
        setIsModalOpen(true);
    };

    // Handle save user
    const handleSaveUser = async (data: UserUpdate) => {
        if (selectedUser) {
            await updateUser(selectedUser.id, data);
            showNotification('success', 'User updated successfully');
        }
        await fetchUsers();
    };

    // Handle delete user
    const handleDeleteClick = (user: User) => {
        setUserToDelete(user);
        setIsDeleteModalOpen(true);
    };

    const handleDeleteConfirm = async () => {
        if (!userToDelete) return;

        try {
            setDeleteLoading(true);
            await deleteUser(userToDelete.id);
            showNotification('success', 'User deleted successfully');
            setIsDeleteModalOpen(false);
            setUserToDelete(null);
            await fetchUsers();
        } catch (error: any) {
            // Extract error message from various error formats
            let errorMessage = 'Failed to delete user';

            if (error.response?.data) {
                const data = error.response.data;
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMessage = data.detail.map((err: any) => err.msg || err).join(', ');
                }
            }

            showNotification('error', errorMessage);
        } finally {
            setDeleteLoading(false);
        }
    };

    // Handle toggle status
    const handleToggleStatus = async (user: User) => {
        try {
            await toggleUserStatus(user.id, !user.is_active);
            showNotification('success', `User ${!user.is_active ? 'activated' : 'deactivated'} successfully`);
            await fetchUsers();
        } catch (error: any) {
            let errorMessage = 'Failed to update user status';

            if (error.response?.data) {
                const data = error.response.data;
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMessage = data.detail.map((err: any) => err.msg || err).join(', ');
                }
            }

            showNotification('error', errorMessage);
        }
    };

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
                    animation: 'slideIn 0.3s ease',
                }}>
                    {notification.message}
                </div>
            )}

            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Users Management</h3>
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <input
                            type="text"
                            placeholder="Search users..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            style={{
                                padding: '0.5rem 1rem',
                                border: '1px solid rgba(0, 0, 0, 0.08)',
                                borderRadius: '8px',
                                fontSize: '0.875rem',
                                width: '200px',
                            }}
                        />
                        <button
                            onClick={handleCreateUser}
                            className="card-action"
                            style={{ cursor: 'pointer' }}
                        >
                            Add User +
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div style={{ padding: '2rem', textAlign: 'center', color: '#86868b' }}>
                        Loading users...
                    </div>
                ) : users.length === 0 ? (
                    <div style={{ padding: '2rem', textAlign: 'center', color: '#86868b' }}>
                        No users found
                    </div>
                ) : (
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Email</th>
                                    <th>Username</th>
                                    <th>Full Name</th>
                                    <th>Status</th>
                                    <th>Role</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => (
                                    <tr key={user.id}>
                                        <td>#{user.id}</td>
                                        <td>{user.email}</td>
                                        <td>{user.username || '-'}</td>
                                        <td>{user.full_name || '-'}</td>
                                        <td>
                                            <span className={`status-badge status-${user.is_active ? 'active' : 'inactive'}`}>
                                                {user.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td>
                                            <span style={{
                                                fontSize: '0.8rem',
                                                fontWeight: '600',
                                                color: user.is_superuser ? '#0071e3' : '#666'
                                            }}>
                                                {user.role_display_name || (user.is_superuser ? 'Super Admin' : 'User')}
                                            </span>
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                <button
                                                    onClick={() => handleEditUser(user)}
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
                                                    Edit
                                                </button>
                                                <button
                                                    onClick={() => handleToggleStatus(user)}
                                                    style={{
                                                        padding: '0.25rem 0.75rem',
                                                        fontSize: '0.75rem',
                                                        background: '#f5f5f7',
                                                        border: 'none',
                                                        borderRadius: '6px',
                                                        cursor: 'pointer',
                                                        color: user.is_active ? '#ff9f0a' : '#34c759',
                                                        fontWeight: '600',
                                                    }}
                                                >
                                                    {user.is_active ? 'Deactivate' : 'Activate'}
                                                </button>
                                                <button
                                                    onClick={() => handleDeleteClick(user)}
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
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* User Modal */}
            <UserModal
                user={selectedUser}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSave={handleSaveUser}
            />

            {/* Delete Confirmation Modal */}
            <DeleteConfirmModal
                isOpen={isDeleteModalOpen}
                title="Delete User"
                message={`Are you sure you want to delete ${userToDelete?.email}? This action cannot be undone.`}
                onConfirm={handleDeleteConfirm}
                onCancel={() => {
                    setIsDeleteModalOpen(false);
                    setUserToDelete(null);
                }}
                loading={deleteLoading}
            />

            <style jsx>{`
        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `}</style>
        </DashboardLayout>
    );
}
