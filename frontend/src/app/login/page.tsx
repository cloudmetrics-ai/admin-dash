/**
 * Login Page
 * ==========
 * 
 * User login page with email/password authentication.
 * Integrates with backend API and redirects to dashboard on success.
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import AuthLayout from '@/components/layouts/AuthLayout';
import Logo from '@/components/ui/Logo';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Checkbox from '@/components/ui/Checkbox';
import { login } from '@/lib/auth';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [mfaRequired, setMfaRequired] = useState(false);
    const [tempToken, setTempToken] = useState('');
    const [mfaCode, setMfaCode] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await login({ email, password });

            // Check if MFA is required
            if ('mfa_required' in response && response.mfa_required) {
                setMfaRequired(true);
                setTempToken(response.temp_token);
                setLoading(false);
                return;
            }

            // Login successful - redirect
            router.push('/admin');
        } catch (err: any) {
            console.error('Login error:', err);

            // Handle different error scenarios
            if (err.response?.status === 401) {
                setError('Invalid email or password');
            } else if (err.response?.data?.detail) {
                setError(err.response.data.detail);
            } else {
                setError('An error occurred. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleMFASubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const { verifyMFA } = await import('@/lib/mfa');
            await verifyMFA(tempToken, mfaCode);

            // MFA verified - redirect
            router.push('/admin');
        } catch (err: any) {
            console.error('MFA verification error:', err);
            setError(err.response?.data?.detail || 'Invalid verification code');
        } finally {
            setLoading(false);
        }
    };

    return (
        <AuthLayout>
            <Logo />

            {!mfaRequired ? (
                <form onSubmit={handleSubmit}>
                    <Input
                        type="email"
                        label="Email"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        autoComplete="email"
                    />

                    <Input
                        type="password"
                        label="Password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        autoComplete="current-password"
                    />

                    <div
                        style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginBottom: 'var(--spacing-lg)',
                        }}
                    >
                        <Checkbox
                            label="Remember me"
                            checked={rememberMe}
                            onChange={(e) => setRememberMe(e.target.checked)}
                        />

                        <Link
                            href="/forgot-password"
                            style={{
                                fontSize: 'var(--font-size-sm)',
                                color: 'var(--color-primary)',
                                textDecoration: 'none',
                                fontWeight: 'var(--font-weight-medium)',
                            }}
                        >
                            Forgot password?
                        </Link>
                    </div>

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
                        {loading ? 'Signing in...' : 'Sign In'}
                    </Button>
                </form>
            ) : (
                <form onSubmit={handleMFASubmit}>
                    <div style={{ marginBottom: 'var(--spacing-lg)', textAlign: 'center' }}>
                        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                            Two-Factor Authentication
                        </h2>
                        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
                            Enter the 6-digit code from your authenticator app
                        </p>
                    </div>

                    <div style={{ textAlign: 'center' }}>
                        <label
                            style={{
                                display: 'block',
                                fontSize: 'var(--font-size-sm)',
                                fontWeight: 'var(--font-weight-semibold)',
                                color: 'var(--color-text-primary)',
                                marginBottom: 'var(--spacing-sm)',
                                textAlign: 'center',
                            }}
                        >
                            Verification Code
                        </label>
                        <input
                            type="text"
                            placeholder="000000"
                            value={mfaCode}
                            onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                            required
                            maxLength={6}
                            autoFocus
                            style={{
                                width: '100%',
                                maxWidth: '400px',
                                padding: '0.875rem 1rem',
                                fontSize: '1.5rem',
                                textAlign: 'center',
                                letterSpacing: '0.5rem',
                                border: 'var(--border-width) solid var(--color-border)',
                                borderRadius: 'var(--border-radius-md)',
                                background: 'var(--color-background-alt)',
                                color: 'var(--color-text-primary)',
                                marginBottom: 'var(--spacing-lg)',
                            }}
                        />
                    </div>

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

                    <Button type="submit" loading={loading} disabled={loading || mfaCode.length !== 6}>
                        {loading ? 'Verifying...' : 'Verify'}
                    </Button>

                    <button
                        type="button"
                        onClick={() => {
                            setMfaRequired(false);
                            setMfaCode('');
                            setError('');
                        }}
                        style={{
                            width: '100%',
                            marginTop: 'var(--spacing-md)',
                            padding: 'var(--spacing-md)',
                            background: 'transparent',
                            border: 'none',
                            color: 'var(--color-primary)',
                            cursor: 'pointer',
                            fontSize: 'var(--font-size-sm)',
                            fontWeight: 'var(--font-weight-medium)',
                        }}
                    >
                        ← Back to login
                    </button>
                </form>
            )}

            <div
                style={{
                    textAlign: 'center',
                    marginTop: 'var(--spacing-xl)',
                    fontSize: 'var(--font-size-sm)',
                    color: 'var(--color-text-secondary)',
                }}
            >
                Don't have an account?{' '}
                <Link
                    href="/register"
                    style={{
                        color: 'var(--color-primary)',
                        textDecoration: 'none',
                        fontWeight: 'var(--font-weight-semibold)',
                    }}
                >
                    Sign up
                </Link>
            </div>
        </AuthLayout>
    );
}
