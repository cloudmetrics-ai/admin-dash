'use client';

/**
 * Admin Dashboard Home Page
 * =========================
 * 
 * Main dashboard page with stats, charts, and tables.
 */

import React from 'react';

import DashboardLayout from '@/components/layouts/DashboardLayout';
import StatsCard from '@/components/dashboard/StatsCard';
import RevenueChart from '@/components/dashboard/RevenueChart';
import ActivityFeed from '@/components/dashboard/ActivityFeed';
import OrdersTable from '@/components/dashboard/OrdersTable';
import '../../styles/dashboard.css';

export default function AdminDashboard() {
    return (
        <DashboardLayout>
            {/* Stats Grid */}
            <div className="stats-grid">
                <StatsCard
                    title="Total Revenue"
                    value="$45,231"
                    change="↑ 12.5% from last month"
                    icon="💵"
                />
                <StatsCard
                    title="Active Users"
                    value="2,845"
                    change="↑ 8.2% from last month"
                    icon="👤"
                />
                <StatsCard
                    title="New Orders"
                    value="1,234"
                    change="↓ 3.1% from last month"
                    icon="🛒"
                    isNegative
                />
                <StatsCard
                    title="Conversion Rate"
                    value="3.24%"
                    change="↑ 1.8% from last month"
                    icon="📊"
                />
            </div>

            {/* Content Grid */}
            <div className="content-grid">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Revenue Overview</h3>
                        <a href="#" className="card-action">View Details →</a>
                    </div>
                    <RevenueChart />
                </div>

                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Recent Activity</h3>
                        <a href="#" className="card-action">View All →</a>
                    </div>
                    <ActivityFeed />
                </div>
            </div>

            {/* Recent Orders Table */}
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Recent Orders</h3>
                    <a href="#" className="card-action">View All →</a>
                </div>
                <OrdersTable />
            </div>
        </DashboardLayout>
    );
}
