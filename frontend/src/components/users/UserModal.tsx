/**
 * UserModal Component
 * ===================
 * 
 * Modal for creating and editing users.
 */

'use client';

import React, { useState, useEffect } from 'react';
import { User, UserUpdate } from '@/lib/users';
import { getRoles, RoleListItem } from '@/lib/roles';
import Input from '../ui/Input';
import Button from '../ui/Button';
import Checkbox from '../ui/Checkbox';

interface UserModalProps {
    user?: User | null;
    isOpen: boolean;
    onClose: () => void;
    onSave: (data: UserUpdate) => Promise<void>;
}

export default function UserModal({ user, isOpen, onClose, onSave }: UserModalProps) {
    const [formData, setFormData] = useState<UserUpdate>({
        email: '',
        username: '',
        full_name: '',
        is_active: true,
        is_superuser: false,
        role_id: null,
    });
    const [roles, setRoles] = useState<RoleListItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch roles for the dropdown
        const fetchRoles = async () => {
            try {
                const data = await getRoles();
                setRoles(data);
            } catch (err) {
                console.error('Failed to fetch roles:', err);
            }
        };

        if (isOpen) {
            fetchRoles();
        }

        if (user) {
            setFormData({
                email: user.email,
                username: user.username || '',
                full_name: user.full_name || '',
                is_active: user.is_active,
                is_superuser: user.is_superuser,
                role_id: user.role_id || null,
            });
        } else {
            setFormData({
                email: '',
                username: '',
                full_name: '',
                is_active: true,
                is_superuser: false,
                role_id: null,
            });
        }
        setError('');
    }, [user, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await onSave(formData);
            onClose();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to save user');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
        }}>
            <div style={{
                background: '#fff',
                borderRadius: '12px',
                padding: '2rem',
                maxWidth: '500px',
                width: '100%',
                maxHeight: '90vh',
                overflow: 'auto',
            }}>
                <h2 style={{
                    fontSize: '1.5rem',
                    fontWeight: '700',
                    marginBottom: '1.5rem',
                    color: '#1d1d1f',
                }}>
                    {user ? 'Edit User' : 'Create User'}
                </h2>

                <form onSubmit={handleSubmit}>
                    <Input
                        label="Email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        required
                    />

                    <Input
                        label="Username"
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    />

                    <Input
                        label="Full Name"
                        type="text"
                        value={formData.full_name}
                        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    />

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.5rem', color: '#1d1d1f' }}>
                            Role
                        </label>
                        <select
                            value={formData.role_id || ''}
                            onChange={(e) => setFormData({ ...formData, role_id: e.target.value ? parseInt(e.target.value) : null })}
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(0,0,0,0.1)',
                                background: '#f5f5f7',
                                fontSize: '1rem',
                                appearance: 'none',
                                outline: 'none',
                            }}
                        >
                            <option value="">Select a role</option>
                            {roles.map(role => (
                                <option key={role.id} value={role.id}>
                                    {role.display_name} {role.is_system_role ? '(System)' : ''}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <Checkbox
                            label="Active"
                            checked={formData.is_active}
                            onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                        />
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <Checkbox
                            label="Superuser"
                            checked={formData.is_superuser}
                            onChange={(e) => setFormData({ ...formData, is_superuser: e.target.checked })}
                        />
                    </div>

                    {error && (
                        <div style={{
                            padding: '0.75rem',
                            background: '#fee',
                            color: '#c00',
                            borderRadius: '8px',
                            marginBottom: '1rem',
                            fontSize: '0.875rem',
                        }}>
                            {error}
                        </div>
                    )}

                    <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                        <Button
                            type="button"
                            variant="secondary"
                            onClick={onClose}
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            variant="primary"
                            loading={loading}
                        >
                            {user ? 'Update' : 'Create'}
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
}
