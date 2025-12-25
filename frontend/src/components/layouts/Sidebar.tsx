/**
 * Sidebar Component
 * =================
 * 
 * Navigation sidebar for the admin dashboard with menu items and logout button.
 */

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { logout } from '@/lib/auth';

const menuItems = [
    { icon: '📊', label: 'Dashboard', href: '/admin' },
    { icon: '👥', label: 'Users', href: '/admin/users' },
    { icon: '🛡️', label: 'Roles', href: '/admin/roles' },
    { icon: '📦', label: 'Products', href: '/admin/products' },
    { icon: '💰', label: 'Payments', href: '/admin/payments' },
    { icon: '📈', label: 'Analytics', href: '/admin/analytics' },
    { icon: '⚙️', label: 'Settings', href: '/admin/settings' },
    { icon: '🔔', label: 'Notifications', href: '/admin/notifications' },
];

export default function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push('/login');
    };

    return (
        <aside className="sidebar">
            <div className="logo">
                <h1>AdminPanel</h1>
                <p>Management System</p>
            </div>

            <nav>
                <ul className="nav-menu">
                    {menuItems.map((item) => (
                        <li key={item.href} className="nav-item">
                            <Link
                                href={item.href}
                                className={`nav-link ${pathname === item.href ? 'active' : ''}`}
                            >
                                <span className="nav-icon">{item.icon}</span>
                                {item.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>

            <div className="sidebar-footer">
                <button className="logout-btn" onClick={handleLogout}>
                    <span className="nav-icon">⎋</span>
                    Sign Out
                </button>
            </div>
        </aside>
    );
}
