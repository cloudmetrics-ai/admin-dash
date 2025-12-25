/**
 * Logo Component
 * ==============
 * 
 * Reusable logo component with icon and text.
 */

import React from 'react';

export interface LogoProps {
    showText?: boolean;
    size?: 'sm' | 'md' | 'lg';
}

export const Logo: React.FC<LogoProps> = ({ showText = true, size = 'md' }) => {
    const sizes = {
        sm: { icon: 48, text: '1.25rem' },
        md: { icon: 64, text: '1.75rem' },
        lg: { icon: 80, text: '2rem' },
    };

    const currentSize = sizes[size];

    return (
        <div
            style={{
                textAlign: 'center',
                marginBottom: showText ? 'var(--spacing-2xl)' : 'var(--spacing-lg)',
            }}
        >
            <div
                className="logo-icon"
                style={{
                    width: `${currentSize.icon}px`,
                    height: `${currentSize.icon}px`,
                    background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%)',
                    borderRadius: 'var(--border-radius-lg)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: size === 'sm' ? '1.5rem' : '2rem',
                    marginBottom: showText ? 'var(--spacing-md)' : '0',
                    boxShadow: 'var(--shadow-primary)',
                }}
            >
                🔐
            </div>

            {showText && (
                <>
                    <h1
                        style={{
                            fontSize: currentSize.text,
                            fontWeight: 'var(--font-weight-bold)',
                            color: 'var(--color-text-primary)',
                            letterSpacing: 'var(--letter-spacing-tight)',
                            marginBottom: 'var(--spacing-xs)',
                        }}
                    >
                        Welcome Back
                    </h1>
                    <p
                        style={{
                            fontSize: 'var(--font-size-base)',
                            color: 'var(--color-text-secondary)',
                            fontWeight: 'var(--font-weight-normal)',
                            letterSpacing: 'var(--letter-spacing-wide)',
                        }}
                    >
                        Sign in to your account
                    </p>
                </>
            )}
        </div>
    );
};

export default Logo;
