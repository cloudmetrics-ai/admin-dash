/**
 * Payments Page
 * =============
 */

import React from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import '../../../styles/dashboard.css';

export default function PaymentsPage() {
    return (
        <DashboardLayout>
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Payments</h3>
                </div>
                <p style={{ color: 'var(--color-text-secondary)', padding: '2rem', textAlign: 'center' }}>
                    Payments management coming soon...
                </p>
            </div>
        </DashboardLayout>
    );
}
