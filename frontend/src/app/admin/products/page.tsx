/**
 * Products Management Page
 * ========================
 * 
 * Page for managing products.
 */

import React from 'react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import '../../../styles/dashboard.css';

export default function ProductsPage() {
    return (
        <DashboardLayout>
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Products Management</h3>
                    <button className="card-action">Add Product +</button>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Category</th>
                                <th>Price</th>
                                <th>Stock</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>#PRD-001</td>
                                <td>Premium Package</td>
                                <td>Subscription</td>
                                <td>$299.00</td>
                                <td>∞</td>
                                <td><span className="status-badge status-active">Active</span></td>
                                <td>
                                    <button style={{ marginRight: '0.5rem', padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>Edit</button>
                                    <button style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>Delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td>#PRD-002</td>
                                <td>Standard Plan</td>
                                <td>Subscription</td>
                                <td>$149.00</td>
                                <td>∞</td>
                                <td><span className="status-badge status-active">Active</span></td>
                                <td>
                                    <button style={{ marginRight: '0.5rem', padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>Edit</button>
                                    <button style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>Delete</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </DashboardLayout>
    );
}
