'use client';

/**
 * Reset Password Page
 * ===================
 * 
 * Page for resetting password using token from email.
 */

import React, { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import AuthLayout from '@/components/layouts/AuthLayout';
import Logo from '@/components/ui/Logo';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import api from '@/lib/api';

function ResetPasswordForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [token, setToken] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        const tokenParam = searchParams.get('token');
        if (tokenParam) {
            setToken(tokenParam);
        } else {
            setError('Invalid reset link. Please request a new password reset.');
        }
    }, [searchParams]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (newPassword.length < 8) {
            setError('Password must be at least 8 characters');
            return;
        }

        setLoading(true);

        try {
            await api.post('/api/v1/auth/reset-password', {
                token,
                new_password: newPassword,
            });
            setSuccess(true);

            // Redirect to login after 3 seconds
            setTimeout(() => {
                router.push('/login');
            }, 3000);
        } catch (err: any) {
            console.error('Reset password error:', err);
            setError(err.response?.data?.detail || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <AuthLayout>
                <Logo />

                <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
                    <div style={{
                        width: '64px',
                        height: '64px',
                        margin: '0 auto var(--spacing-lg)',
                        background: '#34c759',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '2rem',
                        color: '#fff',
                    }}>
                        ✓
                    </div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                        Password Reset Successful
                    </h2>
                    <p style={{ color: 'var(--color-text-secondary)' }}>
                        Your password has been reset. Redirecting to login...
                    </p>
                </div>
            </AuthLayout>
        );
    }

    return (
        <AuthLayout>
            <Logo />

            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                    Reset Your Password
                </h2>
                <p style={{ color: 'var(--color-text-secondary)' }}>
                    Enter your new password below
                </p>
            </div>

            <form onSubmit={handleSubmit}>
                <Input
                    type="password"
                    label="New Password"
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    minLength={8}
                    autoFocus
                />

                <Input
                    type="password"
                    label="Confirm Password"
                    placeholder="Confirm new password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                />

                {error && (
                    <div
                        style={{
                            padding: 'var(--spacing-md)',
                            marginBottom: 'var(--spacing-lg)',
                            backgroundColor: '#fee',
                            border: '1px solid var(--color-error)',
                            borderRadius: 'var(--border-radius-md)',
                            color: 'var(--color-error)',
                            fontSize: 'var(--font-size-sm)',
                        }}
                    >
                        {error}
                    </div>
                )}

                <Button type="submit" loading={loading} disabled={loading || !token}>
                    {loading ? 'Resetting...' : 'Reset Password'}
                </Button>
            </form>

            <div
                style={{
                    textAlign: 'center',
                    marginTop: 'var(--spacing-xl)',
                    fontSize: 'var(--font-size-sm)',
                    color: 'var(--color-text-secondary)',
                }}
            >
                Remember your password?{' '}
                <Link
                    href="/login"
                    style={{
                        color: 'var(--color-primary)',
                        textDecoration: 'none',
                        fontWeight: 'var(--font-weight-semibold)',
                    }}
                >
                    Sign in
                </Link>
            </div>
        </AuthLayout>
    );
}

export default function ResetPasswordPage() {
    return (
        <Suspense fallback={
            <AuthLayout>
                <Logo />
                <div style={{ textAlign: 'center', padding: '2rem' }}>
                    Loading...
                </div>
            </AuthLayout>
        }>
            <ResetPasswordForm />
        </Suspense>
    );
}
