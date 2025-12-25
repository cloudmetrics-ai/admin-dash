'use client';

/**
 * Email Verification Page
 * =======================
 * 
 * Page for verifying email using token from URL.
 */

import React, { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import AuthLayout from '@/components/layouts/AuthLayout';
import Logo from '@/components/ui/Logo';
import api from '@/lib/api';

function VerifyEmailContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');
    const [message, setMessage] = useState('');

    useEffect(() => {
        const token = searchParams.get('token');
        if (!token) {
            setStatus('error');
            setMessage('Invalid verification link. No token provided.');
            return;
        }

        verifyEmail(token);
    }, [searchParams]);

    const verifyEmail = async (token: string) => {
        try {
            const response = await api.get(`/api/v1/auth/verify-email?token=${token}`);
            setStatus('success');
            setMessage(response.data.message || 'Email verified successfully!');

            // Redirect to login after 3 seconds
            setTimeout(() => {
                router.push('/login');
            }, 3000);
        } catch (err: any) {
            console.error('Verification error:', err);
            setStatus('error');
            setMessage(err.response?.data?.detail || 'Verification failed. Please try again.');
        }
    };

    return (
        <AuthLayout>
            <Logo />

            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
                {status === 'verifying' && (
                    <>
                        <div style={{
                            width: '64px',
                            height: '64px',
                            margin: '0 auto var(--spacing-lg)',
                            border: '4px solid #e0e0e0',
                            borderTop: '4px solid #0071e3',
                            borderRadius: '50%',
                            animation: 'spin 1s linear infinite',
                        }} />
                        <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                            Verifying Your Email
                        </h2>
                        <p style={{ color: 'var(--color-text-secondary)' }}>
                            Please wait while we verify your email address...
                        </p>
                        <style jsx>{`
                            @keyframes spin {
                                0% { transform: rotate(0deg); }
                                100% { transform: rotate(360deg); }
                            }
                        `}</style>
                    </>
                )}

                {status === 'success' && (
                    <>
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
                            Email Verified!
                        </h2>
                        <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-lg)' }}>
                            {message}
                        </p>
                        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
                            Redirecting to login...
                        </p>
                    </>
                )}

                {status === 'error' && (
                    <>
                        <div style={{
                            width: '64px',
                            height: '64px',
                            margin: '0 auto var(--spacing-lg)',
                            background: '#ff3b30',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '2rem',
                            color: '#fff',
                        }}>
                            ✕
                        </div>
                        <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>
                            Verification Failed
                        </h2>
                        <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-lg)' }}>
                            {message}
                        </p>
                        <Link
                            href="/login"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                background: '#0071e3',
                                color: '#fff',
                                textDecoration: 'none',
                                borderRadius: '8px',
                                fontWeight: '600',
                            }}
                        >
                            Go to Login
                        </Link>
                    </>
                )}
            </div>
        </AuthLayout>
    );
}

export default function VerifyEmailPage() {
    return (
        <Suspense fallback={
            <AuthLayout>
                <Logo />
                <div style={{ textAlign: 'center', padding: '2rem' }}>
                    Loading...
                </div>
            </AuthLayout>
        }>
            <VerifyEmailContent />
        </Suspense>
    );
}
