/**
 * StatsCard Component
 * ===================
 * 
 * Reusable stat card component for displaying metrics.
 */

import React from 'react';

export interface StatsCardProps {
    title: string;
    value: string | number;
    change: string;
    icon: string;
    isNegative?: boolean;
}

export default function StatsCard({ title, value, change, icon, isNegative = false }: StatsCardProps) {
    return (
        <div className="stat-card">
            <div className="stat-header">
                <div>
                    <div className="stat-title">{title}</div>
                </div>
                <div className="stat-icon">{icon}</div>
            </div>
            <div className="stat-value">{value}</div>
            <div className={`stat-change ${isNegative ? 'negative' : ''}`}>{change}</div>
        </div>
    );
}
