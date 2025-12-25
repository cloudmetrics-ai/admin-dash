/**
 * Topbar Component
 * ================
 * 
 * Top bar with welcome message and user avatar for the admin dashboard.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { getCurrentUser } from '@/lib/auth';

export default function Topbar() {
    const [user, setUser] = useState<any>(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getCurrentUser();
                setUser(userData);
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        };

        fetchUser();
    }, []);

    const getInitials = () => {
        if (!user) return 'AD';
        if (user.full_name) {
            const names = user.full_name.split(' ');
            return names.map((n: string) => n[0]).join('').toUpperCase().slice(0, 2);
        }
        if (user.username) {
            return user.username.slice(0, 2).toUpperCase();
        }
        return user.email.slice(0, 2).toUpperCase();
    };

    return (
        <div className="top-bar">
            <div className="welcome">
                <h2>Welcome back, {user?.full_name || user?.username || 'Admin'}</h2>
                <p>Here's what's happening with your business today</p>
            </div>
            <div className="user-info">
                <div className="user-avatar">{getInitials()}</div>
            </div>
        </div>
    );
}
