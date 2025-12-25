/**
 * Dashboard Page (Redirect)
 * =========================
 * 
 * Redirects to the new admin dashboard.
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';

export default function DashboardPage() {
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated()) {
            router.push('/login');
        } else {
            router.push('/admin');
        }
    }, [router]);

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            color: '#86868b'
        }}>
            Redirecting to admin dashboard...
        </div>
    );
}
