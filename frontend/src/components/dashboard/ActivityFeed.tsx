/**
 * ActivityFeed Component
 * ======================
 * 
 * Recent activity list for the dashboard.
 */

import React from 'react';

interface Activity {
    icon: string;
    title: string;
    time: string;
}

const activities: Activity[] = [
    { icon: '✅', title: 'New order received', time: '2 minutes ago' },
    { icon: '👤', title: 'New user registered', time: '15 minutes ago' },
    { icon: '💰', title: 'Payment processed', time: '1 hour ago' },
    { icon: '📦', title: 'Product shipped', time: '3 hours ago' },
];

export default function ActivityFeed() {
    return (
        <ul className="activity-list">
            {activities.map((activity, index) => (
                <li key={index} className="activity-item">
                    <div className="activity-icon">{activity.icon}</div>
                    <div className="activity-content">
                        <div className="activity-title">{activity.title}</div>
                        <div className="activity-time">{activity.time}</div>
                    </div>
                </li>
            ))}
        </ul>
    );
}
