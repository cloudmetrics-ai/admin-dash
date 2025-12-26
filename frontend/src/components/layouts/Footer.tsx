/**
 * Footer Component
 * ================
 * 
 * Thin footer for the admin dashboard.
 */

'use client';

import React from 'react';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="dashboard-footer">
            <div className="footer-content">
                <p>© {currentYear} CloudMetrics AI. All rights reserved.</p>
                <div className="footer-links">
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                    <a href="#">Support</a>
                </div>
            </div>
        </footer>
    );
}
