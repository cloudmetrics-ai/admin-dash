"""
Fix user_id types in users.py
"""
import re

# Read the file
with open('app/api/v1/users.py', 'r') as f:
    content = f.read()

# Replace all instances of "user_id: int" with "user_id: str"
content = content.replace('user_id: int,', 'user_id: str,')
content = content.replace('user_id: int)', 'user_id: str)')

# Write back
with open('app/api/v1/users.py', 'w') as f:
    f.write(content)

print("✅ Fixed user_id types from int to str")
