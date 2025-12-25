'use client';

/**
 * RoleModal Component
 * ===================
 * 
 * Modal for creating and editing roles and their permissions.
 */

import React, { useState, useEffect } from 'react';
import {
    Role,
    RoleListItem,
    RoleCreate,
    RoleUpdate,
    getPermissions,
    PermissionsByCategory,
    assignRolePermissions
} from '@/lib/roles';
import Input from '../ui/Input';
import Button from '../ui/Button';
import Checkbox from '../ui/Checkbox';

interface RoleModalProps {
    role?: RoleListItem | null; // Summarized role from the list
    isOpen: boolean;
    onClose: () => void;
    onSave: (data: RoleCreate | RoleUpdate) => Promise<void>;
}

export default function RoleModal({ role, isOpen, onClose, onSave }: RoleModalProps) {
    const [formData, setFormData] = useState<RoleCreate | RoleUpdate>({
        display_name: '',
        description: '',
        name: '', // Only for create
    });
    const [allPermissions, setAllPermissions] = useState<PermissionsByCategory[]>([]);
    const [selectedPermissions, setSelectedPermissions] = useState<number[]>([]);
    const [loading, setLoading] = useState(false);
    const [dataLoading, setDataLoading] = useState(false);
    const [error, setError] = useState('');

    // Fetch all available permissions and current role details
    useEffect(() => {
        if (!isOpen) return;

        const fetchData = async () => {
            setDataLoading(true);
            try {
                // Fetch all permissions once
                const perms = await getPermissions();
                setAllPermissions(perms);

                if (role) {
                    // Fetch full role details to get permissions
                    const { getRole } = await import('@/lib/roles');
                    const fullRole = await getRole(role.id);

                    setFormData({
                        display_name: fullRole.display_name,
                        description: fullRole.description || '',
                    });
                    setSelectedPermissions(fullRole.permissions.map(p => p.id));
                } else {
                    setFormData({
                        name: '',
                        display_name: '',
                        description: '',
                    });
                    setSelectedPermissions([]);
                }
            } catch (err: any) {
                console.error('Error fetching role data:', err);
                setError('Failed to load role details');
            } finally {
                setDataLoading(false);
            }
        };

        fetchData();
        setError('');
    }, [role, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // 1. Save Role Info
            await onSave(formData);

            // 2. Save Permissions if not a new role (or if onSave handles it)
            // If we are creating, we might need the new ID first.
            // For now, let's assume onSave handles create/update of base info.
            // If it's an update, let's save permissions too.
            if (role) {
                await assignRolePermissions(role.id, selectedPermissions);
            }
            // For creation, we'd need to handle permission assignment after the role is created.
            // Simplification: We'll update the parent to handle this or just show role created.

            onClose();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to save role');
        } finally {
            setLoading(false);
        }
    };

    const handlePermissionToggle = (id: number) => {
        if (role?.is_system_role) return; // Cannot change system role permissions via this UI for safety

        setSelectedPermissions(prev =>
            prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
        );
    };

    const handleSelectCategory = (categoryPermissions: number[], checked: boolean) => {
        if (role?.is_system_role) return;

        if (checked) {
            setSelectedPermissions(prev => [...new Set([...prev, ...categoryPermissions])]);
        } else {
            setSelectedPermissions(prev => prev.filter(id => !categoryPermissions.includes(id)));
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
                maxWidth: '800px',
                width: '95%',
                maxHeight: '90vh',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
            }}>
                <h2 style={{
                    fontSize: '1.5rem',
                    fontWeight: '700',
                    marginBottom: '1.5rem',
                    color: '#1d1d1f',
                }}>
                    {role ? `Edit Role: ${role.display_name}` : 'Create New Role'}
                    {role?.is_system_role && <span style={{ fontSize: '0.8rem', color: '#86868b', marginLeft: '0.5rem' }}>(System Role - Read Only)</span>}
                </h2>

                {dataLoading ? (
                    <div style={{ padding: '2rem', textAlign: 'center' }}>Loading...</div>
                ) : (
                    <form onSubmit={handleSubmit} style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column', flex: 1 }}>
                        <div style={{ overflowY: 'auto', paddingRight: '0.5rem' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                {!role && (
                                    <Input
                                        label="System Name (snake_case)"
                                        type="text"
                                        placeholder="e.g. content_manager"
                                        value={(formData as RoleCreate).name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        required
                                    />
                                )}
                                <Input
                                    label="Display Name"
                                    type="text"
                                    placeholder="e.g. Content Manager"
                                    value={formData.display_name}
                                    onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                                    required
                                    disabled={role?.is_system_role}
                                />
                            </div>

                            <Input
                                label="Description"
                                type="text"
                                placeholder="What can this role do?"
                                value={formData.description || ''}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                disabled={role?.is_system_role}
                            />

                            <div style={{ marginTop: '1.5rem' }}>
                                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.75rem', color: '#1d1d1f' }}>
                                    Permissions
                                </label>

                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1.5rem' }}>
                                    {allPermissions.map((group) => {
                                        const groupIds = group.permissions.map(p => p.id);
                                        const allSelected = groupIds.every(id => selectedPermissions.includes(id));

                                        return (
                                            <div key={group.category} style={{
                                                border: '1px solid #f5f5f7',
                                                borderRadius: '8px',
                                                padding: '1rem',
                                                background: '#fafafa'
                                            }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', borderBottom: '1px solid #eee', paddingBottom: '0.5rem' }}>
                                                    <span style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', color: '#86868b' }}>
                                                        {group.category}
                                                    </span>
                                                    {!role?.is_system_role && (
                                                        <button
                                                            type="button"
                                                            onClick={() => handleSelectCategory(groupIds, !allSelected)}
                                                            style={{ fontSize: '0.7rem', color: '#0071e3', background: 'none', border: 'none', cursor: 'pointer' }}
                                                        >
                                                            {allSelected ? 'None' : 'All'}
                                                        </button>
                                                    )}
                                                </div>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                                    {group.permissions.map((perm) => (
                                                        <Checkbox
                                                            key={perm.id}
                                                            label={perm.action}
                                                            checked={selectedPermissions.includes(perm.id)}
                                                            onChange={() => handlePermissionToggle(perm.id)}
                                                            disabled={role?.is_system_role}
                                                        />
                                                    ))}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>

                        {error && (
                            <div style={{
                                padding: '0.75rem',
                                background: '#fee',
                                color: '#c00',
                                borderRadius: '8px',
                                marginTop: '1rem',
                                fontSize: '0.875rem',
                            }}>
                                {error}
                            </div>
                        )}

                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid #f5f5f7' }}>
                            <Button
                                type="button"
                                variant="secondary"
                                onClick={onClose}
                                disabled={loading}
                            >
                                Close
                            </Button>
                            {!role?.is_system_role && (
                                <Button
                                    type="submit"
                                    variant="primary"
                                    loading={loading}
                                >
                                    {role ? 'Update Role' : 'Create Role'}
                                </Button>
                            )}
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}
