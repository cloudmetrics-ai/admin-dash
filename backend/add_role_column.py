"""
Add role_id column to users table
"""
from app.core.database import engine
from sqlalchemy import text

def add_role_column():
    """Add role_id column to users table"""
    with engine.connect() as conn:
        # Add the column
        conn.execute(text(
            'ALTER TABLE users ADD COLUMN IF NOT EXISTS role_id INTEGER'
        ))
        
        # Add the foreign key constraint
        conn.execute(text(
            'ALTER TABLE users ADD CONSTRAINT fk_users_role_id '
            'FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL'
        ))
        
        conn.commit()
        print("✅ Added role_id column to users table")

if __name__ == "__main__":
    add_role_column()
