/**
 * Sidebar Component
 * =================
 * 
 * Navigation sidebar for the admin dashboard with menu items and logout button.
 * Implements role-based access control to show only permitted menu items.
 */

'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { logout, getCurrentUser, User } from '@/lib/auth';
import {
    LayoutDashboard,
    Users,
    Shield,
    Package,
    CreditCard,
    TrendingUp,
    Settings,
    Bell,
    LogOut
} from 'lucide-react';

interface MenuItem {
    icon: React.ComponentType<{ className?: string }>;
    label: string;
    href: string;
    requiredPermission?: string; // Optional permission required to view this item
}

const menuItems: MenuItem[] = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/admin' }, // No permission required
    { icon: Users, label: 'Users', href: '/admin/users', requiredPermission: 'users.read' },
    { icon: Shield, label: 'Roles', href: '/admin/roles', requiredPermission: 'roles.read' },
    { icon: Package, label: 'Products', href: '/admin/products', requiredPermission: 'products.read' },
    { icon: CreditCard, label: 'Payments', href: '/admin/payments', requiredPermission: 'payments.read' },
    { icon: TrendingUp, label: 'Analytics', href: '/admin/analytics', requiredPermission: 'analytics.read' },
    { icon: Settings, label: 'Settings', href: '/admin/settings' }, // No permission required
    { icon: Bell, label: 'Notifications', href: '/admin/notifications' }, // No permission required
];

interface SidebarProps {
    isCollapsed: boolean;
    onToggle: () => void;
}

export default function Sidebar({ isCollapsed, onToggle }: SidebarProps) {
    const pathname = usePathname();
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [filteredMenuItems, setFilteredMenuItems] = useState<MenuItem[]>([]);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getCurrentUser();
                setUser(userData);

                // Filter menu items based on permissions
                const visibleItems = menuItems.filter(item => {
                    // If no permission required, show to all authenticated users
                    if (!item.requiredPermission) {
                        return true;
                    }

                    // Superusers see everything
                    if (userData.is_superuser) {
                        return true;
                    }

                    // Check if user has the required permission
                    return userData.permissions?.includes(item.requiredPermission) || false;
                });

                setFilteredMenuItems(visibleItems);
            } catch (error) {
                console.error('Error fetching user:', error);
                // On error, show only items without permission requirements
                setFilteredMenuItems(menuItems.filter(item => !item.requiredPermission));
            }
        };

        fetchUser();
    }, []);

    const handleLogout = () => {
        logout();
        router.push('/login');
    };

    return (
        <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <div className="logo">
                <div className="logo-content">
                    <h1>{isCollapsed ? 'AP' : 'AdminPanel'}</h1>
                    {!isCollapsed && <p>Management System</p>}
                </div>
                <button className="sidebar-toggle" onClick={onToggle} aria-label="Toggle sidebar">
                    {isCollapsed ? '→' : '←'}
                </button>
            </div>

            <nav>
                <ul className="nav-menu">
                    {filteredMenuItems.map((item) => {
                        const IconComponent = item.icon;
                        return (
                            <li key={item.href} className="nav-item">
                                <Link
                                    href={item.href}
                                    className={`nav-link ${pathname === item.href ? 'active' : ''}`}
                                    title={item.label}
                                >
                                    <IconComponent className="nav-icon" />
                                    {!isCollapsed && item.label}
                                </Link>
                            </li>
                        );
                    })}
                </ul>
            </nav>
        </aside>
    );
}
