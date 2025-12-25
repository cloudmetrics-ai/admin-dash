"""
Add roles router to main.py
"""

# Read the file
with open('app/main.py', 'r') as f:
    lines = f.readlines()

# Find the line with "# TODO: Include other routers"
for i, line in enumerate(lines):
    if '# TODO: Include other routers' in line:
        # Insert roles router before this line
        roles_router_code = """# Include roles router
# All routes from this router will be prefixed with /api/v1/roles
app.include_router(
    roles.router,
    prefix=settings.API_V1_STR,
    tags=["roles"]
)

"""
        lines.insert(i, roles_router_code)
        break

# Write back
with open('app/main.py', 'w') as f:
    f.writelines(lines)

print("✅ Added roles router to main.py")
