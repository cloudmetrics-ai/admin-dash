/**
 * AuthLayout Component
 * ====================
 * 
 * Shared layout for authentication pages (login, register).
 * Provides consistent styling and structure.
 */

import React from 'react';

export interface AuthLayoutProps {
    children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
    return (
        <div
            style={{
                background: 'var(--color-background-gradient)',
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 'var(--spacing-xl)',
            }}
        >
            <div
                className="auth-container animate-fade-in"
                style={{
                    background: 'var(--color-background)',
                    borderRadius: 'var(--border-radius-xl)',
                    boxShadow: 'var(--shadow-lg)',
                    border: `var(--border-width) solid var(--color-border-light)`,
                    padding: 'var(--spacing-3xl) var(--spacing-2xl)',
                    width: '100%',
                    maxWidth: '420px',
                }}
            >
                {children}
            </div>
        </div>
    );
};

export default AuthLayout;
