#!/bin/bash

# Project Customization Script
# =============================
# Customize the template for your project

set -e

echo "🎨 Project Customization Script"
echo "================================"
echo ""

# Get project details
read -p "Enter your project name (e.g., 'My Awesome App'): " PROJECT_NAME
read -p "Enter project slug (e.g., 'my-awesome-app'): " PROJECT_SLUG
read -p "Enter project description: " PROJECT_DESC
read -p "Enter your name/organization: " AUTHOR_NAME

echo ""
echo "Customizing project..."
echo ""

# Update backend configuration
echo "📝 Updating backend configuration..."
sed -i '' "s/PROJECT_NAME = \"Admin Dashboard API\"/PROJECT_NAME = \"$PROJECT_NAME API\"/" backend/app/core/config.py
sed -i '' "s/Learn App/$PROJECT_NAME/g" backend/app/services/email_service.py

# Update frontend package.json
echo "📝 Updating frontend configuration..."
sed -i '' "s/\"name\": \"frontend\"/\"name\": \"$PROJECT_SLUG-frontend\"/" frontend/package.json
sed -i '' "s/Learn App/$PROJECT_NAME/g" frontend/src/app/layout.tsx

# Update Docker Compose
echo "📝 Updating Docker configuration..."
sed -i '' "s/learn_postgres/${PROJECT_SLUG}_postgres/" docker-compose.yml
sed -i '' "s/learn_backend/${PROJECT_SLUG}_backend/" docker-compose.yml
sed -i '' "s/learn_frontend/${PROJECT_SLUG}_frontend/" docker-compose.yml
sed -i '' "s/learn_network/${PROJECT_SLUG}_network/" docker-compose.yml

# Update README
echo "📝 Updating documentation..."
cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESC

## Quick Start

### Docker Deployment
\`\`\`bash
./setup.sh
\`\`\`

### Local Development
\`\`\`bash
./dev-setup.sh
./dev-start.sh
\`\`\`

## Documentation

- [Template Guide](./TEMPLATE.md)
- [CRUD Operations](./CRUD_GUIDE.md)
- [Architecture](./ARCHITECTURE.md)
- [Development](./DEVELOPMENT.md)

## Features

- ✅ Authentication (Email/Password, MFA)
- ✅ Email Verification
- ✅ Password Reset
- ✅ Role-Based Access Control
- ✅ Docker Support
- ✅ Local Development Setup

## Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy
**Frontend:** Next.js 14, TypeScript, React

## Author

$AUTHOR_NAME

## License

MIT
EOF

echo ""
echo "✅ Customization complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Update .env files with your configuration"
echo "  2. Customize branding colors in frontend/src/app/globals.css"
echo "  3. Replace logo in frontend/public/"
echo "  4. Update SMTP settings in backend/.env"
echo "  5. Run ./setup.sh or ./dev-setup.sh to start"
echo ""
