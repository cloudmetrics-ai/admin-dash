/**
 * MFA API Client
 * ==============
 * 
 * Functions for Multi-Factor Authentication management.
 */

import api from './api';

export interface MFASetupResponse {
    secret: string;
    qr_code: string;
    backup_codes: string[];
}

export interface MFAStatusResponse {
    mfa_enabled: boolean;
}

/**
 * Get MFA status for current user
 */
export const getMFAStatus = async (): Promise<MFAStatusResponse> => {
    const response = await api.get<MFAStatusResponse>('/api/v1/auth/mfa/status');
    return response.data;
};

/**
 * Setup MFA - get QR code and backup codes
 */
export const setupMFA = async (): Promise<MFASetupResponse> => {
    const response = await api.post<MFASetupResponse>('/api/v1/auth/mfa/setup');
    return response.data;
};

/**
 * Enable MFA with verification code
 */
export const enableMFA = async (secret: string, code: string): Promise<void> => {
    await api.post('/api/v1/auth/mfa/enable', null, {
        params: { secret, code }
    });
};

/**
 * Disable MFA
 */
export const disableMFA = async (password: string): Promise<void> => {
    await api.post('/api/v1/auth/mfa/disable', { password });
};

/**
 * Verify MFA code during login
 */
export const verifyMFA = async (tempToken: string, code: string) => {
    const response = await api.post('/api/v1/auth/mfa/verify', {
        temp_token: tempToken,
        code: code
    });

    // Store tokens
    if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
    }

    return response.data;
};
