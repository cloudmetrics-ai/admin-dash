"""
Add roles and permissions tables

Revision ID: 002
Revises: 001
Create Date: 2025-12-25

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime


# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_system_role', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)
    op.create_index(op.f('ix_permissions_category'), 'permissions', ['category'], unique=False)
    
    # Create role_permissions association table
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('granted_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['granted_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add role_id to users table
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_users_role_id'), 'users', ['role_id'], unique=False)
    op.create_foreign_key('fk_users_role_id', 'users', 'roles', ['role_id'], ['id'], ondelete='SET NULL')
    
    # Seed initial roles
    roles_table = table('roles',
        column('id', sa.Integer),
        column('name', sa.String),
        column('display_name', sa.String),
        column('description', sa.String),
        column('is_system_role', sa.Boolean),
        column('created_at', sa.DateTime)
    )
    
    op.bulk_insert(roles_table, [
        {'id': 1, 'name': 'super_admin', 'display_name': 'Super Admin', 
         'description': 'Full system access including role management', 
         'is_system_role': True, 'created_at': datetime.utcnow()},
        {'id': 2, 'name': 'admin', 'display_name': 'Admin', 
         'description': 'Manage users and core business operations', 
         'is_system_role': True, 'created_at': datetime.utcnow()},
        {'id': 3, 'name': 'manager', 'display_name': 'Manager', 
         'description': 'Manage specific areas without full admin access', 
         'is_system_role': True, 'created_at': datetime.utcnow()},
        {'id': 4, 'name': 'analyst', 'display_name': 'Analyst', 
         'description': 'View and analyze data without modification rights', 
         'is_system_role': True, 'created_at': datetime.utcnow()},
        {'id': 5, 'name': 'user', 'display_name': 'User', 
         'description': 'Standard user with minimal permissions', 
         'is_system_role': True, 'created_at': datetime.utcnow()},
    ])
    
    # Seed initial permissions
    permissions_table = table('permissions',
        column('id', sa.Integer),
        column('name', sa.String),
        column('category', sa.String),
        column('action', sa.String),
        column('description', sa.String),
        column('created_at', sa.DateTime)
    )
    
    permissions_data = [
        # System permissions
        (1, 'system.*', 'system', 'all', 'All system permissions'),
        (2, 'roles.create', 'roles', 'create', 'Create new roles'),
        (3, 'roles.read', 'roles', 'read', 'View roles'),
        (4, 'roles.update', 'roles', 'update', 'Update roles'),
        (5, 'roles.delete', 'roles', 'delete', 'Delete roles'),
        (6, 'permissions.assign', 'permissions', 'assign', 'Assign permissions to roles'),
        
        # User permissions
        (10, 'users.create', 'users', 'create', 'Create new users'),
        (11, 'users.read', 'users', 'read', 'View users'),
        (12, 'users.update', 'users', 'update', 'Update user information'),
        (13, 'users.delete', 'users', 'delete', 'Delete users'),
        (14, 'users.assign_role', 'users', 'assign_role', 'Assign roles to users'),
        
        # Product permissions
        (20, 'products.create', 'products', 'create', 'Create products'),
        (21, 'products.read', 'products', 'read', 'View products'),
        (22, 'products.update', 'products', 'update', 'Update products'),
        (23, 'products.delete', 'products', 'delete', 'Delete products'),
        
        # Payment permissions
        (30, 'payments.read', 'payments', 'read', 'View payments'),
        (31, 'payments.refund', 'payments', 'refund', 'Process refunds'),
        
        # Analytics permissions
        (40, 'analytics.read', 'analytics', 'read', 'View analytics'),
        (41, 'analytics.export', 'analytics', 'export', 'Export analytics data'),
        
        # Dashboard permissions
        (50, 'dashboard.read', 'dashboard', 'read', 'View dashboard'),
        
        # Profile permissions
        (60, 'profile.read', 'profile', 'read', 'View own profile'),
        (61, 'profile.update', 'profile', 'update', 'Update own profile'),
        
        # Settings permissions
        (70, 'settings.read', 'settings', 'read', 'View settings'),
        (71, 'settings.update', 'settings', 'update', 'Update settings'),
        
        # Notification permissions
        (80, 'notifications.read', 'notifications', 'read', 'View notifications'),
        (81, 'notifications.send', 'notifications', 'send', 'Send notifications'),
    ]
    
    op.bulk_insert(permissions_table, [
        {'id': p[0], 'name': p[1], 'category': p[2], 'action': p[3], 
         'description': p[4], 'created_at': datetime.utcnow()}
        for p in permissions_data
    ])
    
    # Assign permissions to roles
    role_perms_table = table('role_permissions',
        column('role_id', sa.Integer),
        column('permission_id', sa.Integer),
        column('granted_at', sa.DateTime)
    )
    
    # Super Admin - all permissions
    super_admin_perms = [{'role_id': 1, 'permission_id': p[0], 'granted_at': datetime.utcnow()} 
                         for p in permissions_data]
    
    # Admin - most permissions except role management
    admin_perm_ids = [10, 11, 12, 13, 14, 20, 21, 22, 23, 30, 31, 40, 41, 50, 60, 61, 70, 71, 80, 81]
    admin_perms = [{'role_id': 2, 'permission_id': pid, 'granted_at': datetime.utcnow()} 
                   for pid in admin_perm_ids]
    
    # Manager - limited permissions
    manager_perm_ids = [11, 12, 20, 21, 22, 30, 40, 50, 60, 61, 80, 81]
    manager_perms = [{'role_id': 3, 'permission_id': pid, 'granted_at': datetime.utcnow()} 
                     for pid in manager_perm_ids]
    
    # Analyst - read-only permissions
    analyst_perm_ids = [11, 21, 30, 40, 41, 50, 60, 61, 80]
    analyst_perms = [{'role_id': 4, 'permission_id': pid, 'granted_at': datetime.utcnow()} 
                     for pid in analyst_perm_ids]
    
    # User - minimal permissions
    user_perm_ids = [50, 60, 61, 80]
    user_perms = [{'role_id': 5, 'permission_id': pid, 'granted_at': datetime.utcnow()} 
                  for pid in user_perm_ids]
    
    op.bulk_insert(role_perms_table, super_admin_perms + admin_perms + manager_perms + analyst_perms + user_perms)


def downgrade():
    # Remove foreign key and column from users
    op.drop_constraint('fk_users_role_id', 'users', type_='foreignkey')
    op.drop_index(op.f('ix_users_role_id'), table_name='users')
    op.drop_column('users', 'role_id')
    
    # Drop tables in reverse order
    op.drop_table('role_permissions')
    op.drop_index(op.f('ix_permissions_category'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
