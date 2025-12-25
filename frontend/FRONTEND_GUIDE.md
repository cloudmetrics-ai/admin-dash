# Frontend Development Guide

## 📋 Table of Contents
1. [Project Structure](#project-structure)
2. [Design System](#design-system)
3. [Component Library](#component-library)
4. [Adding a New Page](#adding-a-new-page)
5. [Authentication Flow](#authentication-flow)
6. [API Integration](#api-integration)
7. [Best Practices](#best-practices)

---

## 📁 Project Structure

```
frontend/src/
├── app/                    # Next.js App Router pages
│   ├── login/             # Login page
│   ├── register/          # Registration page
│   ├── dashboard/         # Dashboard page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page (redirects to login)
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # Reusable UI components
│   │   ├── Input.tsx
│   │   ├── Button.tsx
│   │   ├── Checkbox.tsx
│   │   └── Logo.tsx
│   └── layouts/           # Layout components
│       └── AuthLayout.tsx
├── lib/                   # Utilities and API clients
│   ├── api.ts            # Axios instance
│   └── auth.ts           # Authentication functions
└── styles/
    └── design-system.css  # Design tokens and utilities
```

---

## 🎨 Design System

All design tokens are centralized in `src/styles/design-system.css`.

### Using CSS Variables

```tsx
// In your component
<div style={{ color: 'var(--color-primary)' }}>
  Text in primary color
</div>
```

### Available Design Tokens

**Colors:**
- `--color-primary`, `--color-primary-dark`, `--color-primary-light`
- `--color-text-primary`, `--color-text-secondary`
- `--color-background`, `--color-background-alt`
- `--color-error`, `--color-success`, `--color-warning`

**Spacing:**
- `--spacing-xs` through `--spacing-3xl`

**Typography:**
- `--font-size-xs` through `--font-size-3xl`
- `--font-weight-normal`, `--font-weight-semibold`, `--font-weight-bold`

**Borders & Shadows:**
- `--border-radius-sm` through `--border-radius-xl`
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-primary`

---

## 🧩 Component Library

See [COMPONENTS.md](./COMPONENTS.md) for detailed component documentation.

### Quick Reference

```tsx
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Checkbox from '@/components/ui/Checkbox';
import Logo from '@/components/ui/Logo';
import AuthLayout from '@/components/layouts/AuthLayout';
```

---

## ➕ Adding a New Page

### Step 1: Create the Page File

```bash
# Create a new directory for your page
mkdir -p src/app/my-page

# Create the page component
touch src/app/my-page/page.tsx
```

### Step 2: Create the Page Component

```tsx
// src/app/my-page/page.tsx
'use client';

import React from 'react';

export default function MyPage() {
  return (
    <div style={{ padding: 'var(--spacing-xl)' }}>
      <h1 style={{
        fontSize: 'var(--font-size-3xl)',
        fontWeight: 'var(--font-weight-bold)',
        color: 'var(--color-text-primary)',
      }}>
        My New Page
      </h1>
      <p style={{ color: 'var(--color-text-secondary)' }}>
        Content goes here
      </p>
    </div>
  );
}
```

### Step 3: Add Navigation (Optional)

Update your navigation component or add a Link:

```tsx
import Link from 'next/link';

<Link href="/my-page">My Page</Link>
```

### Step 4: Add API Integration (If Needed)

```tsx
import { useEffect, useState } from 'react';
import api from '@/lib/api';

export default function MyPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/api/v1/my-endpoint');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Render your component
}
```

---

## 🔐 Authentication Flow

### How It Works

1. **User visits the app** → Redirected to `/login`
2. **User logs in** → Token stored in localStorage
3. **API requests** → Token automatically added to headers
4. **Protected pages** → Check for token, redirect if missing
5. **User logs out** → Token cleared, redirect to login

### Protecting a Page

```tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';

export default function ProtectedPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  return <div>Protected content</div>;
}
```

### Getting Current User

```tsx
import { getCurrentUser } from '@/lib/auth';

const user = await getCurrentUser();
console.log(user.email, user.username);
```

---

## 🔌 API Integration

### Making API Calls

```tsx
import api from '@/lib/api';

// GET request
const response = await api.get('/api/v1/endpoint');

// POST request
const response = await api.post('/api/v1/endpoint', {
  key: 'value'
});

// PUT request
const response = await api.put('/api/v1/endpoint/123', {
  key: 'updated value'
});

// DELETE request
const response = await api.delete('/api/v1/endpoint/123');
```

### Error Handling

```tsx
try {
  const response = await api.get('/api/v1/data');
  setData(response.data);
} catch (error: any) {
  if (error.response?.status === 404) {
    console.error('Not found');
  } else if (error.response?.data?.detail) {
    console.error(error.response.data.detail);
  } else {
    console.error('An error occurred');
  }
}
```

---

## ✅ Best Practices

### 1. Use the Design System

Always use CSS variables instead of hardcoded values:

```tsx
// ✅ Good
<div style={{ color: 'var(--color-primary)' }}>

// ❌ Bad
<div style={{ color: '#0071e3' }}>
```

### 2. Reuse Components

Use existing components instead of creating new ones:

```tsx
// ✅ Good
import Button from '@/components/ui/Button';
<Button>Click me</Button>

// ❌ Bad
<button style={{ /* custom styles */ }}>Click me</button>
```

### 3. Handle Loading States

Always show loading indicators:

```tsx
const [loading, setLoading] = useState(false);

<Button loading={loading}>Submit</Button>
```

### 4. Validate Forms

Validate user input before submitting:

```tsx
const validateEmail = (email: string) => {
  return /\S+@\S+\.\S+/.test(email);
};

if (!validateEmail(email)) {
  setError('Invalid email');
  return;
}
```

### 5. Use TypeScript

Define interfaces for your data:

```tsx
interface User {
  id: string;
  email: string;
  username: string;
}

const [user, setUser] = useState<User | null>(null);
```

---

## 🚀 Next Steps

1. Explore the [Component Documentation](./COMPONENTS.md)
2. Check the backend API docs at http://localhost:8000/docs
3. Build your first custom page following this guide
4. Add more reusable components as needed

---

**Happy coding! 🎉**
