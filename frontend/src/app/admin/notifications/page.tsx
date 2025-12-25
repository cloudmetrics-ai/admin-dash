/**
 * Notifications Page
 * ==================
 */

import React from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import '../../../styles/dashboard.css';

export default function NotificationsPage() {
    return (
        <DashboardLayout>
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Notifications</h3>
                </div>
                <p style={{ color: 'var(--color-text-secondary)', padding: '2rem', textAlign: 'center' }}>
                    Notifications page coming soon...
                </p>
            </div>
        </DashboardLayout>
    );
}
