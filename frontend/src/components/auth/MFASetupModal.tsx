'use client';

/**
 * MFA Setup Modal
 * ===============
 * 
 * Modal for setting up Multi-Factor Authentication.
 * Shows QR code, manual entry key, verification, and backup codes.
 */

import React, { useState, useEffect } from 'react';
import { setupMFA, enableMFA, MFASetupResponse } from '@/lib/mfa';

interface MFASetupModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export default function MFASetupModal({ isOpen, onClose, onSuccess }: MFASetupModalProps) {
    const [step, setStep] = useState<'loading' | 'scan' | 'verify' | 'backup' | 'complete'>('loading');
    const [setupData, setSetupData] = useState<MFASetupResponse | null>(null);
    const [verificationCode, setVerificationCode] = useState('');
    const [error, setError] = useState<string>('');
    const [isVerifying, setIsVerifying] = useState(false);

    useEffect(() => {
        if (isOpen) {
            initSetup();
        }
    }, [isOpen]);

    const initSetup = async () => {
        try {
            setStep('loading');
            setError('');
            setVerificationCode('');
            const data = await setupMFA();
            setSetupData(data);
            setStep('scan');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to setup MFA');
            setStep('scan');
        }
    };

    const handleContinueFromScan = () => {
        setStep('verify');
    };

    const handleVerify = async () => {
        if (!setupData || !verificationCode || verificationCode.length !== 6) {
            setError('Please enter a 6-digit code');
            return;
        }

        try {
            setIsVerifying(true);
            setError('');
            await enableMFA(setupData.secret, verificationCode);
            setStep('backup');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Invalid verification code');
        } finally {
            setIsVerifying(false);
        }
    };

    const handleComplete = () => {
        setStep('complete');
        onSuccess();
        onClose();
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
    };

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
                maxWidth: '500px',
                width: '90%',
                maxHeight: '90vh',
                overflow: 'auto',
            }}>
                <h2 style={{ margin: '0 0 1.5rem 0', fontSize: '1.5rem', fontWeight: '700' }}>
                    Enable Two-Factor Authentication
                </h2>

                {error && (
                    <div style={{
                        padding: '1rem',
                        background: '#fee',
                        color: '#c00',
                        borderRadius: '8px',
                        marginBottom: '1rem',
                    }}>
                        {error}
                    </div>
                )}

                {step === 'loading' && (
                    <div style={{ textAlign: 'center', padding: '2rem' }}>
                        <p>Setting up MFA...</p>
                    </div>
                )}

                {step === 'scan' && setupData && (
                    <div>
                        <p style={{ marginBottom: '1rem', color: '#666' }}>
                            <strong>Step 1:</strong> Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)
                        </p>

                        <div style={{
                            display: 'flex',
                            justifyContent: 'center',
                            padding: '1.5rem',
                            background: '#f5f5f7',
                            borderRadius: '8px',
                            marginBottom: '1rem',
                        }}>
                            <img
                                src={setupData.qr_code}
                                alt="MFA QR Code"
                                style={{ width: '200px', height: '200px' }}
                            />
                        </div>

                        <div style={{
                            background: '#f5f5f7',
                            padding: '1rem',
                            borderRadius: '8px',
                            marginBottom: '1rem',
                        }}>
                            <p style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                Manual Entry Key:
                            </p>
                            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                <code style={{
                                    flex: 1,
                                    padding: '0.5rem',
                                    background: '#fff',
                                    borderRadius: '4px',
                                    fontSize: '0.875rem',
                                }}>
                                    {setupData.secret}
                                </code>
                                <button
                                    onClick={() => copyToClipboard(setupData.secret)}
                                    style={{
                                        padding: '0.5rem 1rem',
                                        background: '#0071e3',
                                        color: '#fff',
                                        border: 'none',
                                        borderRadius: '6px',
                                        cursor: 'pointer',
                                        fontSize: '0.875rem',
                                    }}
                                >
                                    Copy
                                </button>
                            </div>
                        </div>

                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                            <button
                                onClick={onClose}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: '#f5f5f7',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    fontWeight: '600',
                                }}
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleContinueFromScan}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: '#0071e3',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    fontWeight: '600',
                                }}
                            >
                                Continue
                            </button>
                        </div>
                    </div>
                )}

                {step === 'verify' && setupData && (
                    <div>
                        <p style={{ marginBottom: '1rem', color: '#666' }}>
                            <strong>Step 2:</strong> Enter the 6-digit code from your authenticator app to verify
                        </p>

                        <input
                            type="text"
                            placeholder="000000"
                            maxLength={6}
                            value={verificationCode}
                            onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, ''))}
                            style={{
                                width: '100%',
                                padding: '1rem',
                                fontSize: '1.5rem',
                                textAlign: 'center',
                                letterSpacing: '0.5rem',
                                border: '2px solid #d1d1d6',
                                borderRadius: '8px',
                                marginBottom: '1rem',
                            }}
                            autoFocus
                        />

                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                            <button
                                onClick={() => setStep('scan')}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: '#f5f5f7',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    fontWeight: '600',
                                }}
                            >
                                Back
                            </button>
                            <button
                                onClick={handleVerify}
                                disabled={isVerifying || verificationCode.length !== 6}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: verificationCode.length === 6 ? '#0071e3' : '#d1d1d6',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: verificationCode.length === 6 ? 'pointer' : 'not-allowed',
                                    fontWeight: '600',
                                }}
                            >
                                {isVerifying ? 'Verifying...' : 'Verify & Enable'}
                            </button>
                        </div>
                    </div>
                )}

                {step === 'backup' && setupData && (
                    <div>
                        <p style={{ marginBottom: '1rem', color: '#666' }}>
                            <strong>Step 3:</strong> Save these backup codes in a safe place. Each code can only be used once.
                        </p>

                        <div style={{
                            background: '#f5f5f7',
                            padding: '1.5rem',
                            borderRadius: '8px',
                            marginBottom: '1rem',
                        }}>
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(2, 1fr)',
                                gap: '0.5rem',
                            }}>
                                {setupData.backup_codes.map((code, index) => (
                                    <code key={index} style={{
                                        padding: '0.5rem',
                                        background: '#fff',
                                        borderRadius: '4px',
                                        fontSize: '0.875rem',
                                        textAlign: 'center',
                                    }}>
                                        {code}
                                    </code>
                                ))}
                            </div>
                        </div>

                        <button
                            onClick={() => copyToClipboard(setupData.backup_codes.join('\n'))}
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                background: '#f5f5f7',
                                border: 'none',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontWeight: '600',
                                marginBottom: '1rem',
                            }}
                        >
                            Copy All Codes
                        </button>

                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                            <button
                                onClick={handleComplete}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: '#34c759',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    fontWeight: '600',
                                }}
                            >
                                I've Saved My Codes
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
