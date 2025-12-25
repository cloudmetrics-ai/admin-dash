# Git Setup Guide

## Initial Setup

This guide helps you initialize Git for this template repository.

---

## Step 1: Initialize Git Repository

```bash
cd /Users/sai/Visual_Studio_Projects/Learn_v1
git init
```

---

## Step 2: Review What Will Be Committed

```bash
git status
```

### Files That WILL Be Committed:
- ✅ Source code (backend/app/, frontend/src/)
- ✅ Configuration files (docker-compose.yml, package.json, requirements.txt)
- ✅ Documentation (*.md files)
- ✅ Scripts (*.sh files)
- ✅ Dockerfiles
- ✅ .env.example files (templates)

### Files That WON'T Be Committed (in .gitignore):
- ❌ .env files (secrets)
- ❌ node_modules/
- ❌ venv/
- ❌ __pycache__/
- ❌ .next/
- ❌ logs/
- ❌ *.pyc files
- ❌ .DS_Store
- ❌ IDE files (.vscode/, .idea/)

---

## Step 3: Add Files

```bash
# Add all files (respecting .gitignore)
git add .

# Or add specific directories
git add backend/ frontend/ docker-compose.yml *.sh *.md
```

---

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Full-stack application template

Features:
- FastAPI backend with PostgreSQL
- Next.js 14 frontend with TypeScript
- Complete authentication system (JWT, MFA, email verification)
- Role-based access control (RBAC)
- Docker deployment setup
- Local development setup
- Comprehensive documentation
- Template customization guides
"
```

---

## Step 5: Add Remote Repository

### GitHub
```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### GitLab
```bash
git remote add origin https://gitlab.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## Step 6: Create .github Folder (Optional)

For GitHub-specific features:

```bash
mkdir -p .github/workflows
```

Add GitHub Actions, issue templates, etc.

---

## Recommended: Add a LICENSE

```bash
# For MIT License
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT License"
```

---

## Recommended: Add CONTRIBUTING.md

```bash
cat > CONTRIBUTING.md << 'EOF'
# Contributing

Thank you for considering contributing to this project!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

See [DEVELOPMENT.md](./DEVELOPMENT.md) for setup instructions.

## Code Style

- Backend: Follow PEP 8 (Python)
- Frontend: Follow TypeScript/React best practices
- Use meaningful commit messages

## Testing

- Add tests for new features
- Ensure all tests pass before submitting PR

## Questions?

Open an issue for discussion.
EOF

git add CONTRIBUTING.md
git commit -m "Add contributing guidelines"
```

---

## Verify Repository is Clean

```bash
# Check status
git status

# View what's ignored
git status --ignored

# Check for large files
find . -type f -size +10M | grep -v node_modules | grep -v venv
```

---

## Useful Git Commands

### Check what will be committed
```bash
git diff --cached
```

### Unstage files
```bash
git reset HEAD <file>
```

### View commit history
```bash
git log --oneline --graph
```

### Create a tag for releases
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git push origin v1.0.0
```

---

## GitHub Template Repository

To make this a GitHub template:

1. Push to GitHub
2. Go to repository Settings
3. Check "Template repository"
4. Users can now click "Use this template" to create their own copy

---

## Best Practices

1. **Never commit secrets** - Use .env.example instead
2. **Keep commits atomic** - One logical change per commit
3. **Write descriptive commit messages**
4. **Review changes before committing** - Use `git diff`
5. **Pull before push** - Avoid conflicts
6. **Use branches** - Don't commit directly to main

---

## Troubleshooting

### Accidentally committed .env
```bash
git rm --cached backend/.env
git commit -m "Remove .env from tracking"
```

### Large file committed
```bash
# Use git-filter-branch or BFG Repo-Cleaner
# See: https://rtyley.github.io/bfg-repo-cleaner/
```

### Reset to clean state
```bash
git clean -fd  # Remove untracked files
git reset --hard HEAD  # Reset to last commit
```

---

Your repository is now ready for Git!
