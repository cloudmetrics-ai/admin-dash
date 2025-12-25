/**
 * Register Page
 * =============
 * 
 * User registration page for creating new accounts.
 * Integrates with backend API and auto-logs in on success.
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import AuthLayout from '@/components/layouts/AuthLayout';
import Logo from '@/components/ui/Logo';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { register, login } from '@/lib/auth';

export default function RegisterPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirmPassword: '',
        fullName: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
        // Clear field error when user types
        if (fieldErrors[name]) {
            setFieldErrors((prev) => ({ ...prev, [name]: '' }));
        }
    };

    const validateForm = (): boolean => {
        const errors: Record<string, string> = {};

        if (!formData.email) {
            errors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            errors.email = 'Email is invalid';
        }

        if (!formData.username) {
            errors.username = 'Username is required';
        } else if (formData.username.length < 3) {
            errors.username = 'Username must be at least 3 characters';
        }

        if (!formData.password) {
            errors.password = 'Password is required';
        } else if (formData.password.length < 8) {
            errors.password = 'Password must be at least 8 characters';
        } else if (!/[A-Z]/.test(formData.password)) {
            errors.password = 'Password must contain at least one uppercase letter';
        } else if (!/[a-z]/.test(formData.password)) {
            errors.password = 'Password must contain at least one lowercase letter';
        } else if (!/[0-9]/.test(formData.password)) {
            errors.password = 'Password must contain at least one digit';
        }

        if (formData.password !== formData.confirmPassword) {
            errors.confirmPassword = 'Passwords do not match';
        }

        setFieldErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            // Register the user
            await register({
                email: formData.email,
                username: formData.username,
                password: formData.password,
                full_name: formData.fullName || undefined,
            });

            // Auto-login after successful registration
            await login({
                email: formData.email,
                password: formData.password,
            });

            // Redirect to dashboard
            router.push('/admin');
        } catch (err: any) {
            console.error('Registration error:', err);

            if (err.response?.data?.detail) {
                const detail = err.response.data.detail;

                if (typeof detail === 'string') {
                    setError(detail);
                } else if (Array.isArray(detail)) {
                    // Pydantic validation errors
                    const errors: Record<string, string> = {};
                    let generalError = '';

                    detail.forEach((item: any) => {
                        if (item.loc && item.msg) {
                            const field = item.loc[item.loc.length - 1];

                            // Map field names to our form fields
                            if (field === 'password' || field === 'email' || field === 'username') {
                                errors[field] = item.msg;
                            } else {
                                generalError += item.msg + '. ';
                            }
                        }
                    });

                    if (Object.keys(errors).length > 0) {
                        setFieldErrors(errors);
                    }
                    if (generalError) {
                        setError(generalError.trim());
                    }
                }
            } else {
                setError('An error occurred during registration. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <AuthLayout>
            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-2xl)' }}>
                <div
                    className="logo-icon"
                    style={{
                        width: '64px',
                        height: '64px',
                        background:
                            'linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%)',
                        borderRadius: 'var(--border-radius-lg)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '2rem',
                        marginBottom: 'var(--spacing-md)',
                        boxShadow: 'var(--shadow-primary)',
                    }}
                >
                    🔐
                </div>

                <h1
                    style={{
                        fontSize: '1.75rem',
                        fontWeight: 'var(--font-weight-bold)',
                        color: 'var(--color-text-primary)',
                        letterSpacing: 'var(--letter-spacing-tight)',
                        marginBottom: 'var(--spacing-xs)',
                    }}
                >
                    Create Account
                </h1>
                <p
                    style={{
                        fontSize: 'var(--font-size-base)',
                        color: 'var(--color-text-secondary)',
                        fontWeight: 'var(--font-weight-normal)',
                        letterSpacing: 'var(--letter-spacing-wide)',
                    }}
                >
                    Sign up to get started
                </p>
            </div>

            <form onSubmit={handleSubmit}>
                <Input
                    type="email"
                    name="email"
                    label="Email"
                    placeholder="you@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    error={fieldErrors.email}
                    required
                    autoComplete="email"
                />

                <Input
                    type="text"
                    name="username"
                    label="Username"
                    placeholder="johndoe"
                    value={formData.username}
                    onChange={handleChange}
                    error={fieldErrors.username}
                    required
                    autoComplete="username"
                />

                <Input
                    type="text"
                    name="fullName"
                    label="Full Name (Optional)"
                    placeholder="John Doe"
                    value={formData.fullName}
                    onChange={handleChange}
                    autoComplete="name"
                />

                <Input
                    type="password"
                    name="password"
                    label="Password"
                    placeholder="At least 8 characters"
                    value={formData.password}
                    onChange={handleChange}
                    error={fieldErrors.password}
                    helperText="Must contain uppercase, lowercase, and a number"
                    required
                    autoComplete="new-password"
                />

                <Input
                    type="password"
                    name="confirmPassword"
                    label="Confirm Password"
                    placeholder="Re-enter your password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    error={fieldErrors.confirmPassword}
                    required
                    autoComplete="new-password"
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
                    {loading ? 'Creating account...' : 'Create Account'}
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
                Already have an account?{' '}
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
