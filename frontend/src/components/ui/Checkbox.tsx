/**
 * Checkbox Component
 * ==================
 * 
 * Styled checkbox component matching the design system.
 */

import React from 'react';

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({
    label,
    className = '',
    ...props
}) => {
    const checkboxId = props.id || props.name;

    return (
        <div
            className={`checkbox-wrapper ${className}`}
            style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--spacing-sm)',
            }}
        >
            <input
                type="checkbox"
                id={checkboxId}
                style={{
                    width: '18px',
                    height: '18px',
                    borderRadius: 'var(--border-radius-sm)',
                    border: `var(--border-width) solid var(--color-border)`,
                    cursor: 'pointer',
                }}
                {...props}
            />
            {label && (
                <label
                    htmlFor={checkboxId}
                    style={{
                        fontSize: 'var(--font-size-sm)',
                        color: 'var(--color-text-primary)',
                        cursor: 'pointer',
                        userSelect: 'none',
                    }}
                >
                    {label}
                </label>
            )}
        </div>
    );
};

export default Checkbox;
