/**
 * OrdersTable Component
 * =====================
 * 
 * Recent orders table for the dashboard.
 */

import React from 'react';

interface Order {
    id: string;
    customer: string;
    product: string;
    amount: string;
    status: 'active' | 'pending' | 'inactive';
    date: string;
}

const orders: Order[] = [
    { id: '#ORD-2024-001', customer: 'John Smith', product: 'Premium Package', amount: '$299.00', status: 'active', date: 'Dec 24, 2025' },
    { id: '#ORD-2024-002', customer: 'Sarah Johnson', product: 'Standard Plan', amount: '$149.00', status: 'pending', date: 'Dec 23, 2025' },
    { id: '#ORD-2024-003', customer: 'Michael Brown', product: 'Enterprise Suite', amount: '$599.00', status: 'active', date: 'Dec 23, 2025' },
    { id: '#ORD-2024-004', customer: 'Emily Davis', product: 'Basic Package', amount: '$99.00', status: 'inactive', date: 'Dec 22, 2025' },
    { id: '#ORD-2024-005', customer: 'David Wilson', product: 'Pro Plan', amount: '$249.00', status: 'active', date: 'Dec 22, 2025' },
];

export default function OrdersTable() {
    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Product</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map((order) => (
                        <tr key={order.id}>
                            <td>{order.id}</td>
                            <td>{order.customer}</td>
                            <td>{order.product}</td>
                            <td>{order.amount}</td>
                            <td>
                                <span className={`status-badge status-${order.status}`}>
                                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                                </span>
                            </td>
                            <td>{order.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
