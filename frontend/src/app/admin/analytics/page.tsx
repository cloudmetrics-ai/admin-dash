/**
 * Analytics Page
 * ==============
 */

import React from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import '../../../styles/dashboard.css';

export default function AnalyticsPage() {
    return (
        <DashboardLayout>
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Analytics</h3>
                </div>
                <p style={{ color: 'var(--color-text-secondary)', padding: '2rem', textAlign: 'center' }}>
                    Analytics dashboard coming soon...
                </p>
            </div>
        </DashboardLayout>
    );
}
