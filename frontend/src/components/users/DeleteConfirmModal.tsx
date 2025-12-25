/**
 * DeleteConfirmModal Component
 * ============================
 * 
 * Confirmation modal for delete operations.
 */

'use client';

import React from 'react';
import Button from '../ui/Button';

interface DeleteConfirmModalProps {
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    onCancel: () => void;
    loading?: boolean;
}

export default function DeleteConfirmModal({
    isOpen,
    title,
    message,
    onConfirm,
    onCancel,
    loading = false,
}: DeleteConfirmModalProps) {
    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
        }}>
            <div style={{
                background: '#fff',
                borderRadius: '12px',
                padding: '2rem',
                maxWidth: '400px',
                width: '100%',
            }}>
                <h2 style={{
                    fontSize: '1.25rem',
                    fontWeight: '700',
                    marginBottom: '1rem',
                    color: '#1d1d1f',
                }}>
                    {title}
                </h2>

                <p style={{
                    color: '#86868b',
                    marginBottom: '1.5rem',
                    lineHeight: '1.5',
                }}>
                    {message}
                </p>

                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                    <Button
                        type="button"
                        variant="secondary"
                        onClick={onCancel}
                        disabled={loading}
                    >
                        Cancel
                    </Button>
                    <Button
                        type="button"
                        variant="primary"
                        onClick={onConfirm}
                        loading={loading}
                        style={{ background: '#ff3b30' }}
                    >
                        Delete
                    </Button>
                </div>
            </div>
        </div>
    );
}
