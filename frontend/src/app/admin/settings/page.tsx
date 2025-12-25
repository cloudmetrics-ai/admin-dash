'use client';

/**
 * User Settings Page
 * ==================
 * 
 * Page for managing user account settings including MFA.
 */

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import MFASetupModal from '@/components/auth/MFASetupModal';
import { getMFAStatus, disableMFA } from '@/lib/mfa';
import { getCurrentUser } from '@/lib/auth';
import '../../../styles/dashboard.css';

export default function SettingsPage() {
    const [mfaEnabled, setMfaEnabled] = useState(false);
    const [loading, setLoading] = useState(true);
    const [showMFASetup, setShowMFASetup] = useState(false);
    const [user, setUser] = useState<any>(null);
    const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [statusData, userData] = await Promise.all([
                getMFAStatus().catch(() => ({ mfa_enabled: false })), // Default to false if error
                getCurrentUser()
            ]);
            setMfaEnabled(statusData.mfa_enabled);
            setUser(userData);
        } catch (error: any) {
            console.error('Error loading settings:', error);
            // If 401/403, user might not be authenticated
            if (error.response?.status === 401 || error.response?.status === 403) {
                // Redirect to login will be handled by API interceptor
                return;
            }
        } finally {
            setLoading(false);
        }
    };

    const showNotification = (type: 'success' | 'error', message: string) => {
        setNotification({ type, message });
        setTimeout(() => setNotification(null), 3000);
    };

    const handleEnableMFA = () => {
        setShowMFASetup(true);
    };

    const handleMFASetupSuccess = () => {
        setMfaEnabled(true);
        showNotification('success', 'MFA enabled successfully!');
    };

    const handleDisableMFA = async () => {
        const password = prompt('Enter your password to disable MFA:');
        if (!password) return;

        try {
            await disableMFA(password);
            setMfaEnabled(false);
            showNotification('success', 'MFA disabled successfully');
        } catch (error: any) {
            showNotification('error', error.response?.data?.detail || 'Failed to disable MFA');
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
                }}>
                    {notification.message}
                </div>
            )}

            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Account Settings</h3>
                </div>

                {loading ? (
                    <div style={{ padding: '2rem', textAlign: 'center', color: '#86868b' }}>
                        Loading...
                    </div>
                ) : (
                    <div style={{ padding: '1.5rem' }}>
                        {/* User Info Section */}
                        <div style={{ marginBottom: '2rem' }}>
                            <h4 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>
                                Profile Information
                            </h4>
                            <div style={{ display: 'grid', gap: '1rem' }}>
                                <div>
                                    <label style={{ fontSize: '0.875rem', color: '#666', display: 'block', marginBottom: '0.25rem' }}>
                                        Email
                                    </label>
                                    <div style={{ fontSize: '1rem', fontWeight: '500' }}>
                                        {user?.email}
                                    </div>
                                </div>
                                <div>
                                    <label style={{ fontSize: '0.875rem', color: '#666', display: 'block', marginBottom: '0.25rem' }}>
                                        Username
                                    </label>
                                    <div style={{ fontSize: '1rem', fontWeight: '500' }}>
                                        {user?.username || '-'}
                                    </div>
                                </div>
                                <div>
                                    <label style={{ fontSize: '0.875rem', color: '#666', display: 'block', marginBottom: '0.25rem' }}>
                                        Full Name
                                    </label>
                                    <div style={{ fontSize: '1rem', fontWeight: '500' }}>
                                        {user?.full_name || '-'}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* MFA Section */}
                        <div style={{
                            padding: '1.5rem',
                            background: '#f5f5f7',
                            borderRadius: '12px',
                        }}>
                            <div style={{ marginBottom: '1rem' }}>
                                <h4 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                    Two-Factor Authentication
                                </h4>
                                <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>
                                    Add an extra layer of security to your account
                                </p>
                            </div>

                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '1rem',
                                marginBottom: mfaEnabled ? '1rem' : 0,
                            }}>
                                <span style={{
                                    padding: '0.5rem 1rem',
                                    borderRadius: '20px',
                                    fontSize: '0.875rem',
                                    fontWeight: '600',
                                    background: mfaEnabled ? '#e1f5fe' : '#fee',
                                    color: mfaEnabled ? '#01579b' : '#c00',
                                }}>
                                    {mfaEnabled ? 'Enabled' : 'Disabled'}
                                </span>
                                {mfaEnabled ? (
                                    <button
                                        onClick={handleDisableMFA}
                                        style={{
                                            padding: '0.75rem 1.5rem',
                                            background: '#ff3b30',
                                            color: '#fff',
                                            border: 'none',
                                            borderRadius: '8px',
                                            cursor: 'pointer',
                                            fontWeight: '600',
                                            fontSize: '0.875rem',
                                        }}
                                    >
                                        Disable MFA
                                    </button>
                                ) : (
                                    <button
                                        onClick={handleEnableMFA}
                                        style={{
                                            padding: '0.75rem 1.5rem',
                                            background: '#0071e3',
                                            color: '#fff',
                                            border: 'none',
                                            borderRadius: '8px',
                                            cursor: 'pointer',
                                            fontWeight: '600',
                                            fontSize: '0.875rem',
                                        }}
                                    >
                                        Enable MFA
                                    </button>
                                )}
                            </div>

                            {mfaEnabled && (
                                <div style={{
                                    padding: '1rem',
                                    background: '#fff',
                                    borderRadius: '8px',
                                }}>
                                    <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>
                                        🔒 Your account is protected with two-factor authentication.
                                        You'll need to enter a code from your authenticator app when logging in.
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>

            <MFASetupModal
                isOpen={showMFASetup}
                onClose={() => setShowMFASetup(false)}
                onSuccess={handleMFASetupSuccess}
            />
        </DashboardLayout>
    );
}
