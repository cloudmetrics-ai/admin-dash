/**
 * Button Component
 * ================
 * 
 * Reusable button component with primary and secondary variants.
 * Includes loading state support.
 */

import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary';
    loading?: boolean;
    children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    loading = false,
    children,
    disabled,
    className = '',
    style = {},
    ...props
}) => {
    const isPrimary = variant === 'primary';

    const baseStyles: React.CSSProperties = {
        width: '100%',
        padding: '0.9375rem 1.5rem',
        fontSize: 'var(--font-size-base)',
        fontWeight: isPrimary ? 'var(--font-weight-semibold)' : 'var(--font-weight-medium)',
        borderRadius: 'var(--border-radius-md)',
        border: isPrimary ? 'none' : `var(--border-width) solid var(--color-border)`,
        cursor: disabled || loading ? 'not-allowed' : 'pointer',
        transition: 'all var(--transition-base)',
        letterSpacing: 'var(--letter-spacing-normal)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 'var(--spacing-sm)',
        opacity: disabled || loading ? 0.6 : 1,
        ...style,
    };

    const primaryStyles: React.CSSProperties = {
        color: '#ffffff',
        background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%)',
        boxShadow: 'var(--shadow-primary)',
    };

    const secondaryStyles: React.CSSProperties = {
        color: 'var(--color-text-primary)',
        background: 'var(--color-background-alt)',
    };

    return (
        <button
            className={`btn btn-${variant} ${className}`}
            style={{
                ...baseStyles,
                ...(isPrimary ? primaryStyles : secondaryStyles),
            }}
            disabled={disabled || loading}
            {...props}
        >
            {loading && (
                <span
                    className="animate-spin"
                    style={{
                        display: 'inline-block',
                        width: '16px',
                        height: '16px',
                        border: '2px solid currentColor',
                        borderRightColor: 'transparent',
                        borderRadius: '50%',
                    }}
                />
            )}
            {children}
        </button>
    );
};

export default Button;
