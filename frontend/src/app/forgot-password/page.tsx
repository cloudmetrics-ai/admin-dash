'use client';

/**
 * Forgot Password Page
 * ====================
 * 
 * Page for requesting password reset email.
 */

import React, { useState } from 'react';
import Link from 'next/link';
import AuthLayout from '@/components/layouts/AuthLayout';
import Logo from '@/components/ui/Logo';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import api from '@/lib/api';

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await api.post('/api/v1/auth/forgot-password', { email });
            setSuccess(true);
        } catch (err: any) {
            console.error('Forgot password error:', err);
            const errorDetail = err.response?.data?.detail;

            if (errorDetail === 'Please verify your email first') {
                setError('Please verify your email address before resetting your password. Check your inbox for the verification link.');
            } else {
                setError(errorDetail || 'An error occurred. Please try again.');
            }
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
                    }}>
                        ✓
                    </div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                        Check Your Email
                    </h2>
                    <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-lg)' }}>
                        If an account exists for {email}, you will receive a password reset link shortly.
                    </p>
                    <Link
                        href="/login"
                        style={{
                            color: 'var(--color-primary)',
                            textDecoration: 'none',
                            fontWeight: 'var(--font-weight-semibold)',
                        }}
                    >
                        ← Back to login
                    </Link>
                </div>
            </AuthLayout>
        );
    }

    return (
        <AuthLayout>
            <Logo />

            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                    Forgot Password?
                </h2>
                <p style={{ color: 'var(--color-text-secondary)' }}>
                    Enter your email and we'll send you a reset link
                </p>
            </div>

            <form onSubmit={handleSubmit}>
                <Input
                    type="email"
                    label="Email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                    autoFocus
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

                <Button type="submit" loading={loading} disabled={loading}>
                    {loading ? 'Sending...' : 'Send Reset Link'}
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
