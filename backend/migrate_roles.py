"""
Database Migration Script for Roles and Permissions
===================================================

Run this script to create roles and permissions tables and seed initial data.

Usage:
    python migrate_roles.py
"""

from app.core.database import engine, SessionLocal
from app.models.role import Role, Permission, Base
from app.models.user import User
from datetime import datetime


def run_migration():
    """Create tables and seed initial data"""
    
    print("Creating tables...")
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    db = SessionLocal()
    
    try:
        # Check if roles already exist
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            print(f"⚠️  Roles already exist ({existing_roles} found). Skipping seed...")
            return
        
        print("\nSeeding roles...")
        # Create roles
        roles_data = [
            {'name': 'super_admin', 'display_name': 'Super Admin', 
             'description': 'Full system access including role management', 'is_system_role': True},
            {'name': 'admin', 'display_name': 'Admin', 
             'description': 'Manage users and core business operations', 'is_system_role': True},
            {'name': 'manager', 'display_name': 'Manager', 
             'description': 'Manage specific areas without full admin access', 'is_system_role': True},
            {'name': 'analyst', 'display_name': 'Analyst', 
             'description': 'View and analyze data without modification rights', 'is_system_role': True},
            {'name': 'user', 'display_name': 'User', 
             'description': 'Standard user with minimal permissions', 'is_system_role': True},
        ]
        
        roles = {}
        for role_data in roles_data:
            role = Role(**role_data)
            db.add(role)
            db.flush()
            roles[role_data['name']] = role
            print(f"  ✓ Created role: {role.display_name}")
        
        print("\nSeeding permissions...")
        # Create permissions
        permissions_data = [
            # System permissions
            ('system.*', 'system', 'all', 'All system permissions'),
            ('roles.create', 'roles', 'create', 'Create new roles'),
            ('roles.read', 'roles', 'read', 'View roles'),
            ('roles.update', 'roles', 'update', 'Update roles'),
            ('roles.delete', 'roles', 'delete', 'Delete roles'),
            ('permissions.assign', 'permissions', 'assign', 'Assign permissions to roles'),
            
            # User permissions
            ('users.create', 'users', 'create', 'Create new users'),
            ('users.read', 'users', 'read', 'View users'),
            ('users.update', 'users', 'update', 'Update user information'),
            ('users.delete', 'users', 'delete', 'Delete users'),
            ('users.assign_role', 'users', 'assign_role', 'Assign roles to users'),
            
            # Product permissions
            ('products.create', 'products', 'create', 'Create products'),
            ('products.read', 'products', 'read', 'View products'),
            ('products.update', 'products', 'update', 'Update products'),
            ('products.delete', 'products', 'delete', 'Delete products'),
            
            # Payment permissions
            ('payments.read', 'payments', 'read', 'View payments'),
            ('payments.refund', 'payments', 'refund', 'Process refunds'),
            
            # Analytics permissions
            ('analytics.read', 'analytics', 'read', 'View analytics'),
            ('analytics.export', 'analytics', 'export', 'Export analytics data'),
            
            # Dashboard permissions
            ('dashboard.read', 'dashboard', 'read', 'View dashboard'),
            
            # Profile permissions
            ('profile.read', 'profile', 'read', 'View own profile'),
            ('profile.update', 'profile', 'update', 'Update own profile'),
            
            # Settings permissions
            ('settings.read', 'settings', 'read', 'View settings'),
            ('settings.update', 'settings', 'update', 'Update settings'),
            
            # Notification permissions
            ('notifications.read', 'notifications', 'read', 'View notifications'),
            ('notifications.send', 'notifications', 'send', 'Send notifications'),
        ]
        
        permissions = {}
        for perm_data in permissions_data:
            perm = Permission(
                name=perm_data[0],
                category=perm_data[1],
                action=perm_data[2],
                description=perm_data[3]
            )
            db.add(perm)
            db.flush()
            permissions[perm_data[0]] = perm
            print(f"  ✓ Created permission: {perm.name}")
        
        print("\nAssigning permissions to roles...")
        # Assign permissions to roles
        
        # Super Admin - all permissions
        roles['super_admin'].permissions = list(permissions.values())
        print(f"  ✓ Assigned {len(permissions)} permissions to Super Admin")
        
        # Admin - most permissions except role management
        admin_perms = [p for name, p in permissions.items() 
                      if not name.startswith('system.') and not name.startswith('roles.') 
                      and not name.startswith('permissions.')]
        roles['admin'].permissions = admin_perms
        print(f"  ✓ Assigned {len(admin_perms)} permissions to Admin")
        
        # Manager - limited permissions
        manager_perm_names = [
            'users.read', 'users.update',
            'products.create', 'products.read', 'products.update',
            'payments.read', 'analytics.read',
            'dashboard.read', 'profile.read', 'profile.update',
            'notifications.read', 'notifications.send'
        ]
        roles['manager'].permissions = [permissions[name] for name in manager_perm_names]
        print(f"  ✓ Assigned {len(manager_perm_names)} permissions to Manager")
        
        # Analyst - read-only permissions
        analyst_perm_names = [
            'users.read', 'products.read', 'payments.read',
            'analytics.read', 'analytics.export',
            'dashboard.read', 'profile.read', 'profile.update',
            'notifications.read'
        ]
        roles['analyst'].permissions = [permissions[name] for name in analyst_perm_names]
        print(f"  ✓ Assigned {len(analyst_perm_names)} permissions to Analyst")
        
        # User - minimal permissions
        user_perm_names = [
            'dashboard.read', 'profile.read', 'profile.update', 'notifications.read'
        ]
        roles['user'].permissions = [permissions[name] for name in user_perm_names]
        print(f"  ✓ Assigned {len(user_perm_names)} permissions to User")
        
        db.commit()
        print("\n✅ Migration completed successfully!")
        print(f"\nCreated {len(roles)} roles and {len(permissions)} permissions")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("RBAC Migration Script")
    print("=" * 60)
    run_migration()
