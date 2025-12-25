/**
 * Dashboard Layout Component
 * ==========================
 * 
 * Main layout wrapper for the admin dashboard with sidebar and content area.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import '../../styles/dashboard.css';

interface DashboardLayoutProps {
    children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
    const router = useRouter();
    const [isClient, setIsClient] = useState(false);
    const [isChecking, setIsChecking] = useState(true);

    useEffect(() => {
        // Mark as client-side rendered
        setIsClient(true);

        // Protect the dashboard - redirect to login if not authenticated
        if (!isAuthenticated()) {
            router.push('/login');
        } else {
            setIsChecking(false);
        }
    }, [router]);

    // During SSR, show nothing
    if (!isClient) {
        return null;
    }

    // If not authenticated, show loading while redirecting
    if (!isAuthenticated() || isChecking) {
        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh',
                background: '#f5f5f7',
            }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{
                        width: '40px',
                        height: '40px',
                        border: '4px solid #e0e0e0',
                        borderTop: '4px solid #0071e3',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite',
                        margin: '0 auto 1rem',
                    }} />
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>
                        Checking authentication...
                    </p>
                </div>
                <style jsx>{`
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}</style>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            <Sidebar />
            <main className="main-content">
                <Topbar />
                {children}
            </main>
        </div>
    );
}
