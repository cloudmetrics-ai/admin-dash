/**
 * Input Component
 * ===============
 * 
 * Reusable input component with label, error message, and helper text support.
 * Styled according to the design system.
 */

import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ label, error, helperText, className = '', ...props }, ref) => {
        const inputId = props.id || props.name;

        return (
            <div className="form-group" style={{ marginBottom: 'var(--spacing-lg)' }}>
                {label && (
                    <label
                        htmlFor={inputId}
                        className="form-label"
                        style={{
                            display: 'block',
                            fontSize: 'var(--font-size-sm)',
                            fontWeight: 'var(--font-weight-semibold)',
                            color: 'var(--color-text-primary)',
                            marginBottom: 'var(--spacing-sm)',
                            letterSpacing: 'var(--letter-spacing-wide)',
                        }}
                    >
                        {label}
                    </label>
                )}

                <input
                    ref={ref}
                    id={inputId}
                    className={`form-input ${className}`}
                    style={{
                        width: '100%',
                        padding: '0.875rem 1rem',
                        fontSize: 'var(--font-size-base)',
                        border: `var(--border-width) solid ${error ? 'var(--color-error)' : 'var(--color-border)'}`,
                        borderRadius: 'var(--border-radius-md)',
                        background: 'var(--color-background-alt)',
                        color: 'var(--color-text-primary)',
                        transition: 'all var(--transition-base)',
                        letterSpacing: 'var(--letter-spacing-wide)',
                        ...props.style, // Merge custom styles
                    }}
                    {...props}
                />

                {error && (
                    <p
                        style={{
                            marginTop: 'var(--spacing-sm)',
                            fontSize: 'var(--font-size-sm)',
                            color: 'var(--color-error)',
                        }}
                    >
                        {error}
                    </p>
                )}

                {helperText && !error && (
                    <p
                        style={{
                            marginTop: 'var(--spacing-sm)',
                            fontSize: 'var(--font-size-sm)',
                            color: 'var(--color-text-secondary)',
                        }}
                    >
                        {helperText}
                    </p>
                )}
            </div>
        );
    }
);

Input.displayName = 'Input';

export default Input;
