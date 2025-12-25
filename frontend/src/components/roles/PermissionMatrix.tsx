'use client';

/**
 * PermissionMatrix Component
 * =========================
 * 
 * A visual grid showing all roles vs all permissions.
 */

import React, { useState, useEffect } from 'react';
import {
    getRoles,
    getPermissions,
    getRole,
    assignRolePermissions,
    RoleListItem,
    PermissionsByCategory,
    Role
} from '@/lib/roles';

export default function PermissionMatrix() {
    const [roles, setRoles] = useState<RoleListItem[]>([]);
    const [permissionsByCategory, setPermissionsByCategory] = useState<PermissionsByCategory[]>([]);
    const [fullRoles, setFullRoles] = useState<Record<number, Role>>({});
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [rolesData, permsData] = await Promise.all([
                    getRoles(),
                    getPermissions()
                ]);
                setRoles(rolesData);
                setPermissionsByCategory(permsData);

                // Fetch full details for each role to get their permissions
                const fullRoleDetails: Record<number, Role> = {};
                await Promise.all(rolesData.map(async (r) => {
                    const full = await getRole(r.id);
                    fullRoleDetails[r.id] = full;
                }));
                setFullRoles(fullRoleDetails);
            } catch (err) {
                console.error('Error fetching matrix data:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const togglePermission = async (roleId: number, permissionId: number) => {
        const role = fullRoles[roleId];
        if (!role || role.is_system_role) return;

        const currentPerms = role.permissions.map(p => p.id);
        const newPerms = currentPerms.includes(permissionId)
            ? currentPerms.filter(id => id !== permissionId)
            : [...currentPerms, permissionId];

        setUpdating(`${roleId}-${permissionId}`);
        try {
            const updatedRole = await assignRolePermissions(roleId, newPerms);
            setFullRoles(prev => ({ ...prev, [roleId]: updatedRole }));
        } catch (err) {
            console.error('Error updating permission:', err);
        } finally {
            setUpdating(null);
        }
    };

    if (loading) {
        return <div style={{ padding: '2rem', textAlign: 'center', color: '#86868b' }}>Loading matrix...</div>;
    }

    return (
        <div style={{ overflowX: 'auto', background: '#fff', borderRadius: '12px', border: '1px solid rgba(0,0,0,0.05)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                    <tr style={{ background: '#f5f5f7' }}>
                        <th style={{ padding: '1rem', borderBottom: '1px solid #eee', position: 'sticky', left: 0, background: '#f5f5f7', zIndex: 10, minWidth: '200px' }}>
                            Permission
                        </th>
                        {roles.map(role => (
                            <th key={role.id} style={{ padding: '1rem', borderBottom: '1px solid #eee', textAlign: 'center', minWidth: '100px' }}>
                                <div style={{ fontSize: '0.8rem', fontWeight: '700' }}>{role.display_name}</div>
                                {role.is_system_role && <div style={{ fontSize: '0.6rem', color: '#86868b' }}>(System)</div>}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {permissionsByCategory.map(category => (
                        <React.Fragment key={category.category}>
                            <tr style={{ background: '#fafafa' }}>
                                <td
                                    colSpan={roles.length + 1}
                                    style={{
                                        padding: '0.5rem 1rem',
                                        fontSize: '0.7rem',
                                        fontWeight: '800',
                                        color: '#86868b',
                                        textTransform: 'uppercase',
                                        letterSpacing: '0.05em',
                                        borderBottom: '1px solid #eee'
                                    }}
                                >
                                    {category.category}
                                </td>
                            </tr>
                            {category.permissions.map(perm => (
                                <tr key={perm.id} style={{ borderBottom: '1px solid #f5f5f7' }}>
                                    <td style={{
                                        padding: '0.75rem 1rem',
                                        fontSize: '0.8rem',
                                        position: 'sticky',
                                        left: 0,
                                        background: '#fff',
                                        zIndex: 5,
                                        color: '#1d1d1f'
                                    }}>
                                        <div style={{ fontWeight: '600' }}>{perm.action}</div>
                                        <div style={{ fontSize: '0.7rem', color: '#86868b' }}>{perm.name}</div>
                                    </td>
                                    {roles.map(role => {
                                        const hasPermission = fullRoles[role.id]?.permissions.some(p => p.id === perm.id);
                                        const isUpdating = updating === `${role.id}-${perm.id}`;

                                        return (
                                            <td
                                                key={role.id}
                                                onClick={() => !role.is_system_role && togglePermission(role.id, perm.id)}
                                                style={{
                                                    textAlign: 'center',
                                                    cursor: role.is_system_role ? 'default' : 'pointer',
                                                    background: isUpdating ? '#f0f7ff' : 'transparent',
                                                    transition: 'background 0.2s'
                                                }}
                                            >
                                                {isUpdating ? (
                                                    <span style={{ fontSize: '0.8rem' }}>...</span>
                                                ) : hasPermission ? (
                                                    <span style={{ color: '#34c759', fontSize: '1.2rem', fontWeight: 'bold' }}>✓</span>
                                                ) : (
                                                    <span style={{ color: '#ff3b30', opacity: 0.2 }}>-</span>
                                                )}
                                            </td>
                                        );
                                    })}
                                </tr>
                            ))}
                        </React.Fragment>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
